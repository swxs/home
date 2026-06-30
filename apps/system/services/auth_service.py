# -*- coding: utf-8 -*-
# @File    : services/auth_service.py
# @AUTH    : code_creater

import uuid
import logging
import secrets
from typing import Dict, Optional
from urllib.parse import urlencode

import httpx
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import core
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
from ..repositories.user_identity_repository import UserIdentityRepository
from ..schemas.user import UserSchema
from ..schemas.user_auth import UserAuthOut, UserAuthSchema

logger = logging.getLogger("main.apps.system.services.auth_service")


class AuthService:
    """认证业务层：refresh_token/token/signin、GitHub OAuth 登录与回调（含多表事务与外部 HTTP）。

    身份查询/写入委托 UserIdentityRepository（返回 ORM、仅 flush）；事务边界在本层用
    transaction(db) 显式控制，只读路径不包事务。RedirectResponse 等 HTTP 响应对象在
    api 层构造，本层只返回业务数据。
    """

    def __init__(self, db: AsyncSession, identity_repo: Optional[UserIdentityRepository] = None):
        self.db = db
        self.identity_repo = identity_repo or UserIdentityRepository(db)

    async def refresh_token(self, ttype: int, identifier: str, credential: str) -> Dict[str, str]:
        # 使用 Schema 构建查询条件
        user_auth_schema = UserAuthSchema(ttype=ttype, identifier=identifier, credential=credential)

        # 单表只读：直接走 identity repo，不包事务
        user_auth = await self.identity_repo.find_user_auth(user_auth_schema)

        if not user_auth:
            raise exceptions.Http403ForbiddenException(
                exceptions.Http403ForbiddenException.PasswordError, "账号信息不正确"
            )

        # 生成jwt
        token_schema = TokenSchema(
            user_id=str(user_auth.user_id),
        )
        token = tokener.encode(**token_schema.model_dump())
        refresh_token = refresh_tokener.encode(**token_schema.model_dump())

        return {
            "token": token,
            "refresh_token": refresh_token,
        }

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

        # 生成jwt
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

    async def github_login(self) -> Dict[str, str]:
        """GitHub OAuth登录入口，构建重定向到 GitHub 授权页面所需的数据。"""
        if not core.config.GITHUB_CLIENT_ID:
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.NoResource, "GitHub OAuth未配置"
            )

        # 生成state参数用于防止CSRF攻击
        state = secrets.token_urlsafe(32)

        # 将state存储到session或cookie中（这里简化处理，实际应该存储到redis等）
        # 为了简化，我们将state作为查询参数返回，前端需要保存并在回调时验证

        # 构建GitHub授权URL
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
            # 使用code换取access_token
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

            # 使用access_token获取用户信息
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

            # 查找或创建用户（多表写在单一事务内）
            async with transaction(self.db):
                user = await self.identity_repo.resolve_or_create_github_user(
                    github_id=github_id,
                    github_username=github_username,
                    github_email=github_email,
                    access_token=access_token,
                )

            # 生成JWT token
            token_schema = TokenSchema(user_id=str(user.id))
            token = tokener.encode(**token_schema.model_dump())
            refresh_token = refresh_tokener.encode(**token_schema.model_dump())

            # 重定向到前端，带上token
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
