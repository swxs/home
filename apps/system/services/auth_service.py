# -*- coding: utf-8 -*-
# @File    : services/auth_service.py
# @AUTH    : code_creater

import logging
import secrets
import uuid
from typing import Dict, Optional
from urllib.parse import urlencode

import httpx
from fastapi import BackgroundTasks
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import core
from apps.notify.consts import EmailTemplateType, TokenPurpose
from apps.notify.email.services.email_send_service import EmailSendService
from apps.notify.utils.redis_client import RedisTokenStore
from web import exceptions
from web.dependencies.db import get_db
from web.dependencies.transaction import transaction
from web.schemas.token import TokenSchema

# 通用方法
from commons.Helpers import refresh_tokener, tokener
from commons.Helpers.Helper_JWT import (
    ExpiredSignatureError,
    InvalidSignatureError,
)

# 本模块方法
from .. import consts
from ..repositories.user_identity_repository import UserIdentityRepository
from ..schemas.auth import MessageResponse
from ..schemas.user import UserSchema
from ..schemas.user_auth import UserAuthOut, UserAuthSchema
from ..utils.password import hash_password, verify_password

logger = logging.getLogger("main.apps.system.services.auth_service")


class AuthService:
    """认证业务层：refresh_token/token/signin、GitHub OAuth 登录与回调（含多表事务与外部 HTTP）。

    身份查询/写入委托 UserIdentityRepository（返回 ORM、仅 flush）；事务边界在本层用
    transaction(db) 显式控制，只读路径不包事务。RedirectResponse 等 HTTP 响应对象在
    api 层构造，本层只返回业务数据。
    """

    def __init__(
        self,
        db: AsyncSession,
        identity_repo: Optional[UserIdentityRepository] = None,
        email_service: Optional[EmailSendService] = None,
        token_store: Optional[RedisTokenStore] = None,
    ):
        self.db = db
        self.identity_repo = identity_repo or UserIdentityRepository(db)
        self.email_service = email_service or EmailSendService(db)
        self.token_store = token_store or RedisTokenStore()

    async def _require_email_verified(self, user_id: str) -> None:
        email_auth = await self.identity_repo.find_user_auth(
            UserAuthSchema(
                user_id=user_id,
                ttype=consts.UserAuth_Ttype.EMAIL,
            )
        )
        if email_auth is None or email_auth.ifverified != consts.UserAuth_Ifverified.VERIFIED:
            raise exceptions.Http403ForbiddenException(
                exceptions.Http403ForbiddenException.EmailNotVerified,
                "邮箱未验证，请先完成邮箱验证",
            )

    async def _issue_tokens(self, user_id: str) -> Dict[str, str]:
        token_schema = TokenSchema(user_id=str(user_id))
        token = tokener.encode(**token_schema.model_dump())
        refresh_token = refresh_tokener.encode(**token_schema.model_dump())
        return {"token": token, "refresh_token": refresh_token}

    async def _send_verification_email(
        self,
        background_tasks: BackgroundTasks,
        user_id: str,
        email: str,
    ) -> None:
        token = secrets.token_urlsafe(32)
        await self.token_store.set_token(
            TokenPurpose.EMAIL_VERIFY.value,
            token,
            {"user_id": str(user_id)},
            core.config.EMAIL_VERIFY_TOKEN_TTL,
        )
        await self.email_service.schedule_send(
            background_tasks,
            EmailTemplateType.EMAIL_VERIFY,
            email,
            token,
        )

    async def refresh_token(self, ttype: int, identifier: str, credential: str) -> Dict[str, str]:
        user_auth = await self.identity_repo.find_user_auth(
            UserAuthSchema(ttype=ttype, identifier=identifier)
        )

        if not user_auth or not verify_password(credential, user_auth.credential or ""):
            raise exceptions.Http403ForbiddenException(
                exceptions.Http403ForbiddenException.PasswordError, "账号信息不正确"
            )

        await self._require_email_verified(str(user_auth.user_id))
        return await self._issue_tokens(str(user_auth.user_id))

    async def token(self, refresh_token: str) -> Dict[str, str]:
        try:
            header, payload = refresh_tokener.decode(refresh_token)
            user_id = payload.get("user_id")
        except InvalidSignatureError:
            raise exceptions.Http401UnauthorizedException(
                exceptions.Http401UnauthorizedException.TokenIllegal, "token不合法"
            )
        except ExpiredSignatureError:
            raise exceptions.Http401UnauthorizedException(
                exceptions.Http401UnauthorizedException.TokenTimeout, "token已过期"
            )

        token_schema = TokenSchema(
            user_id=str(user_id),
        )
        token = tokener.encode(**token_schema.model_dump())

        return {
            "token": token,
            "refresh_token": refresh_token,
        }

    async def signin(self, user_auth_schema: UserAuthSchema) -> UserAuthOut:
        user_schema = UserSchema(username=f"user_{str(uuid.uuid4())[:6]}")

        async with transaction(self.db):
            _user, user_auth = await self.identity_repo.create_user_with_auth(user_schema, user_auth_schema)

        return UserAuthOut.model_validate(user_auth)

    async def register(
        self,
        username: str,
        email: str,
        password: str,
        background_tasks: BackgroundTasks,
    ) -> MessageResponse:
        if await self.identity_repo.find_user_by_username(username):
            raise exceptions.Http409ConflictException(
                exceptions.Http409ConflictException.ResourceConflict,
                "用户名已存在",
            )
        if await self.identity_repo.find_user_auth(
            UserAuthSchema(ttype=consts.UserAuth_Ttype.EMAIL, identifier=email)
        ):
            raise exceptions.Http409ConflictException(
                exceptions.Http409ConflictException.ResourceConflict,
                "邮箱已被注册",
            )

        password_hash = hash_password(password)
        async with transaction(self.db):
            user, _password_auth, _email_auth = await self.identity_repo.create_user_with_password_and_email(
                username, email, password_hash
            )

        await self._send_verification_email(background_tasks, str(user.id), email)
        return MessageResponse(message="注册成功，请查收验证邮件")

    async def verify_email(self, token: str) -> MessageResponse:
        payload = await self.token_store.get_and_delete_token(TokenPurpose.EMAIL_VERIFY.value, token)
        if payload is None:
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.NoResource,
                "验证链接无效或已过期",
            )

        user_id = payload.get("user_id")
        async with transaction(self.db):
            await self.identity_repo.verify_user_auths(user_id)

        return MessageResponse(message="邮箱验证成功")

    async def resend_verification(self, email: str, background_tasks: BackgroundTasks) -> MessageResponse:
        email_auth = await self.identity_repo.find_user_auth(
            UserAuthSchema(ttype=consts.UserAuth_Ttype.EMAIL, identifier=email)
        )
        if email_auth is None:
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.NoResource,
                "邮箱未注册",
            )
        if email_auth.ifverified == consts.UserAuth_Ifverified.VERIFIED:
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.NoResource,
                "邮箱已验证，无需重发",
            )

        await self._send_verification_email(background_tasks, str(email_auth.user_id), email)
        return MessageResponse(message="验证邮件已重发")

    async def forgot_password(
        self,
        username: str,
        email: str,
        background_tasks: BackgroundTasks,
    ) -> MessageResponse:
        user = await self.identity_repo.find_user_by_username(username)
        if user is None:
            return MessageResponse(message="若账号存在且已激活，重置邮件已发送")

        email_auth = await self.identity_repo.find_user_auth(
            UserAuthSchema(
                user_id=user.id,
                ttype=consts.UserAuth_Ttype.EMAIL,
                identifier=email,
            )
        )
        if email_auth is None:
            return MessageResponse(message="若账号存在且已激活，重置邮件已发送")

        if email_auth.ifverified != consts.UserAuth_Ifverified.VERIFIED:
            await self._send_verification_email(background_tasks, str(user.id), email)
            return MessageResponse(message="账号未激活，已重发验证邮件", unactivated=True)

        token = secrets.token_urlsafe(32)
        await self.token_store.set_token(
            TokenPurpose.PASSWORD_RESET.value,
            token,
            {"user_id": str(user.id)},
            core.config.EMAIL_RESET_TOKEN_TTL,
        )
        await self.email_service.schedule_send(
            background_tasks,
            EmailTemplateType.PASSWORD_RESET,
            email,
            token,
        )
        return MessageResponse(message="若账号存在且已激活，重置邮件已发送")

    async def reset_password(self, token: str, new_password: str) -> MessageResponse:
        payload = await self.token_store.get_and_delete_token(TokenPurpose.PASSWORD_RESET.value, token)
        if payload is None:
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.NoResource,
                "重置链接无效或已过期",
            )

        user_id = payload.get("user_id")
        password_hash = hash_password(new_password)
        async with transaction(self.db):
            await self.identity_repo.update_password_credential(user_id, password_hash)

        return MessageResponse(message="密码重置成功")

    async def github_login(self) -> Dict[str, str]:
        """GitHub OAuth登录入口，构建重定向到 GitHub 授权页面所需的数据。"""
        if not core.config.GITHUB_CLIENT_ID:
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.NoResource, "GitHub OAuth未配置"
            )

        state = secrets.token_urlsafe(32)

        github_auth_url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={core.config.GITHUB_CLIENT_ID}"
            f"&redirect_uri={core.config.GITHUB_REDIRECT_URI}"
            f"&scope=read:user user:email"
            f"&state={state}"
        )

        return {
            "auth_url": github_auth_url,
            "state": state,
        }

    async def github_callback(self, code: str, state: str) -> str:
        """GitHub OAuth回调处理，返回重定向 URL（RedirectResponse 在 api 构造）。"""
        if not core.config.GITHUB_CLIENT_ID or not core.config.GITHUB_CLIENT_SECRET:
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.NoResource, "GitHub OAuth未配置"
            )

        try:
            async with httpx.AsyncClient() as client:
                token_response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": core.config.GITHUB_CLIENT_ID,
                        "client_secret": core.config.GITHUB_CLIENT_SECRET,
                        "code": code,
                    },
                    headers={"Accept": "application/json"},
                )
                token_data = token_response.json()

            if "error" in token_data:
                logger.error(f"GitHub OAuth错误: {token_data}")
                raise exceptions.Http400BadRequestException(
                    exceptions.Http400BadRequestException.NoResource,
                    f"GitHub OAuth错误: {token_data.get('error_description', '未知错误')}",
                )

            access_token = token_data.get("access_token")
            if not access_token:
                raise exceptions.Http400BadRequestException(
                    exceptions.Http400BadRequestException.NoResource, "无法获取GitHub access_token"
                )

            async with httpx.AsyncClient() as client:
                user_response = await client.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )
                user_data = user_response.json()

            if "id" not in user_data:
                logger.error(f"GitHub用户信息获取失败: {user_data}")
                raise exceptions.Http400BadRequestException(
                    exceptions.Http400BadRequestException.NoResource, "无法获取GitHub用户信息"
                )

            github_id = str(user_data["id"])
            github_username = user_data.get("login", f"github_{github_id}")
            github_email = user_data.get("email", "")

            async with transaction(self.db):
                user = await self.identity_repo.resolve_or_create_github_user(
                    github_id=github_id,
                    github_username=github_username,
                    github_email=github_email,
                    access_token=access_token,
                )

            token_schema = TokenSchema(user_id=str(user.id))
            token = tokener.encode(**token_schema.model_dump())
            refresh_token = refresh_tokener.encode(**token_schema.model_dump())

            frontend_url = core.config.OAUTH2_LOGIN_URL
            params = urlencode({"token": token, "refresh_token": refresh_token})
            redirect_url = f"{frontend_url}?{params}"

            return redirect_url

        except httpx.HTTPError as e:
            logger.error(f"GitHub OAuth HTTP错误: {e}")
            raise exceptions.Http500InternalServerException(
                exceptions.Http500InternalServerException.UnknownError, "GitHub OAuth请求失败"
            )
        except Exception as e:
            logger.error(f"GitHub OAuth错误: {e}", exc_info=True)
            raise exceptions.Http500InternalServerException(
                exceptions.Http500InternalServerException.UnknownError, f"GitHub OAuth处理失败: {str(e)}"
            )


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)
