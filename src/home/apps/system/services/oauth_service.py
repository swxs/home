# -*- coding: utf-8 -*-
# @File    : services/oauth_service.py
# @AUTH    : code_creater

import logging
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import urlencode

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import home.core as core
from home.web import exceptions
from home.web.dependencies.db import get_db
from home.web.dependencies.transaction import transaction
from home.web.schemas.token import TokenSchema

# 通用方法
from home.commons.Helpers import refresh_tokener, tokener

# 本模块方法
from ..repositories.oauth_authorization_code_repository import (
    OAuthAuthorizationCodeRepository,
)
from ..repositories.oauth_client_repository import OAuthClientRepository
from ..repositories.oauth_user_grant_repository import OAuthUserGrantRepository
from ..repositories.user_repository import UserRepository
from ..schemas.oauth import OAuthTokenResponse, OAuthUserInfoResponse
from ..schemas.oauth_authorization_code import OAuthAuthorizationCodeSchema
from ..schemas.oauth_client import OAuthClientSchema
from ..schemas.user import UserSchema
from ..utils.oauth import (
    build_authorization_url,
    build_consent_redirect_url,
    build_error_redirect_url,
    generate_authorization_code,
    get_authorization_code_expires_at,
    normalize_scope,
    validate_redirect_uri,
)

logger = logging.getLogger("main.apps.system.services.oauth_service")


@dataclass
class OAuthJSONResult:
    """service 层向 api 层回传的 JSON 结果契约（内容 + 状态码），不含 HTTP/CORS 细节。"""

    content: dict
    status_code: int = 200


class OAuthService:
    """OAuth2.0 业务层：authorize/token/userinfo 与授权码签发。

    严格复制原有多段事务与显式 commit；token 的三通道解析（Bearer/Cookie/Query）
    保留在 api 层并将解析出的 user_id 传入。
    """

    def __init__(
        self,
        db: AsyncSession,
        client_repo: Optional[OAuthClientRepository] = None,
        auth_code_repo: Optional[OAuthAuthorizationCodeRepository] = None,
        grant_repo: Optional[OAuthUserGrantRepository] = None,
        user_repo: Optional[UserRepository] = None,
    ):
        self.db = db
        self.client_repo = client_repo or OAuthClientRepository(db)
        self.auth_code_repo = auth_code_repo or OAuthAuthorizationCodeRepository(db)
        self.grant_repo = grant_repo or OAuthUserGrantRepository(db)
        self.user_repo = user_repo or UserRepository(db)

    async def _issue_authorization_code(
        self,
        user_id: str,
        client_id: str,
        redirect_uri: str,
        scope: Optional[str],
        state: Optional[str],
    ) -> str:
        """生成授权码并返回重定向到客户端的 URL（Response 在 api 层构造）。"""
        code = generate_authorization_code()
        expires_at = get_authorization_code_expires_at()

        auth_code_schema = {
            "code": code,
            "client_id": client_id,
            "user_id": user_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "expires_at": expires_at,
            "is_used": False,
        }

        async with transaction(self.db):
            await self.auth_code_repo.create_one(OAuthAuthorizationCodeSchema(**auth_code_schema))

        logger.info(f"生成授权码: {code}, 客户端: {client_id}, 用户: {user_id}")

        redirect_url = build_authorization_url(redirect_uri, code, state)
        return redirect_url

    async def authorize(
        self,
        client_id: str,
        redirect_uri: str,
        response_type: str,
        scope: Optional[str],
        state: Optional[str],
        confirm: Optional[str],
        user_id: Optional[str],
    ) -> str:
        """OAuth2.0授权端点：处理授权请求，返回重定向 URL（Response 在 api 层构造）。

        user_id 由 api 层从 Bearer/Cookie/Query 三通道解析后传入。
        """
        # 验证response_type
        if response_type != "code":
            if redirect_uri:
                error_url = build_error_redirect_url(
                    redirect_uri, "unsupported_response_type", f"不支持的response_type: {response_type}", state
                )
                return error_url
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.InvalidParameter, f"不支持的response_type: {response_type}"
            )

        # 验证客户端
        oauth_client = await self.client_repo.find_one_or_none(OAuthClientSchema(client_id=client_id))

        if not oauth_client:
            if redirect_uri:
                error_url = build_error_redirect_url(redirect_uri, "invalid_client", "无效的客户端ID", state)
                return error_url
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.InvalidParameter, "无效的客户端ID"
            )

        # 验证客户端是否激活
        if oauth_client.is_active != 1:  # 1表示ACTIVE
            if redirect_uri:
                error_url = build_error_redirect_url(redirect_uri, "invalid_client", "客户端未激活", state)
                return error_url
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.InvalidParameter, "客户端未激活"
            )

        # 验证redirect_uri
        if not validate_redirect_uri(oauth_client.redirect_uri, redirect_uri):
            if redirect_uri:
                error_url = build_error_redirect_url(redirect_uri, "invalid_request", "重定向URI不匹配", state)
                return error_url
            raise exceptions.Http400BadRequestException(
                exceptions.Http400BadRequestException.InvalidParameter, "重定向URI不匹配"
            )

        # 如果用户未登录，重定向到登录页面
        if not user_id:
            login_url = core.config.OAUTH2_LOGIN_URL
            params = {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": response_type,
            }
            if scope:
                params["scope"] = scope
            if state:
                params["state"] = state

            separator = "&" if "?" in login_url else "?"
            return f"{login_url}{separator}{urlencode(params)}"

        normalized_scope = normalize_scope(scope)
        grant = await self.grant_repo.find_by_user_client(user_id, client_id)

        if confirm == "true":
            async with transaction(self.db):
                await self.grant_repo.upsert(user_id, client_id, normalized_scope)
            return await self._issue_authorization_code(user_id, client_id, redirect_uri, scope, state)

        if grant and normalize_scope(grant.scope) == normalized_scope:
            return await self._issue_authorization_code(user_id, client_id, redirect_uri, scope, state)

        consent_url = build_consent_redirect_url(
            client_id=client_id,
            redirect_uri=redirect_uri,
            response_type=response_type,
            scope=scope,
            state=state,
        )
        return consent_url

    async def token(
        self,
        grant_type: str,
        code: Optional[str],
        redirect_uri: Optional[str],
        client_id: str,
        client_secret: str,
        refresh_token: Optional[str],
    ) -> OAuthJSONResult:
        """OAuth2.0令牌端点：用授权码换取访问令牌，或使用 refresh_token 刷新令牌。"""
        try:
            logger.info(f"Token请求开始: grant_type={grant_type}, client_id={client_id}")

            # 验证客户端
            oauth_client = await self.client_repo.find_one_or_none(OAuthClientSchema(client_id=client_id))

            if not oauth_client:
                # OAuth2.0标准错误响应格式
                return OAuthJSONResult(
                    content={"error": "invalid_client", "error_description": "无效的客户端ID"},
                    status_code=400,
                )

            # 验证客户端密钥
            if oauth_client.client_secret != client_secret:
                return OAuthJSONResult(
                    content={"error": "invalid_client", "error_description": "无效的客户端密钥"},
                    status_code=400,
                )

            # 验证客户端是否激活
            if oauth_client.is_active != 1:
                return OAuthJSONResult(
                    content={"error": "invalid_client", "error_description": "客户端未激活"},
                    status_code=400,
                )

            if grant_type == "authorization_code":
                # 授权码模式
                if not code or not redirect_uri:
                    return OAuthJSONResult(
                        content={"error": "invalid_request", "error_description": "缺少必要的参数"},
                        status_code=400,
                    )

                # 查找授权码
                auth_code = None
                user_id = None
                scope = None

                auth_code = await self.auth_code_repo.find_one_or_none(OAuthAuthorizationCodeSchema(code=code))

                if not auth_code:
                    logger.warning(f"授权码不存在: {code}")
                    return OAuthJSONResult(
                        content={"error": "invalid_grant", "error_description": "无效的授权码"},
                        status_code=400,
                    )

                # 验证授权码是否已使用
                if auth_code.is_used:
                    logger.warning(f"授权码已使用: {code}")
                    return OAuthJSONResult(
                        content={"error": "invalid_grant", "error_description": "授权码已使用"},
                        status_code=400,
                    )

                if auth_code.expires_at < datetime.utcnow():
                    logger.warning(f"授权码已过期: {code}, 过期时间: {auth_code.expires_at}")
                    return OAuthJSONResult(
                        content={"error": "invalid_grant", "error_description": "授权码已过期"},
                        status_code=400,
                    )

                # 验证授权码是否属于该客户端
                if auth_code.client_id != client_id:
                    logger.warning(
                        f"授权码与客户端不匹配: code={code}, code_client={auth_code.client_id}, request_client={client_id}"
                    )
                    return OAuthJSONResult(
                        content={"error": "invalid_grant", "error_description": "授权码与客户端不匹配"},
                        status_code=400,
                    )

                # 验证redirect_uri是否匹配
                if not validate_redirect_uri(auth_code.redirect_uri, redirect_uri):
                    logger.warning(f"重定向URI不匹配: code_uri={auth_code.redirect_uri}, request_uri={redirect_uri}")
                    return OAuthJSONResult(
                        content={"error": "invalid_request", "error_description": "重定向URI不匹配"},
                        status_code=400,
                    )

                # 标记授权码为已使用（在单独的事务中）
                async with transaction(self.db):
                    await self.auth_code_repo.update_one(
                        str(auth_code.id), OAuthAuthorizationCodeSchema(is_used=True)
                    )

                # 保存user_id和scope以便在事务外使用
                user_id = str(auth_code.user_id)
                scope = auth_code.scope

                # 生成token（在事务提交后）
                token_schema = TokenSchema(user_id=user_id)
                access_token = tokener.encode(**token_schema.model_dump())
                refresh_token_value = refresh_tokener.encode(**token_schema.model_dump())

                logger.info(f"生成token成功: 客户端={client_id}, 用户={user_id}")

                # OAuth2.0标准要求直接返回JSON，不使用包装格式
                response_data = OAuthTokenResponse(
                    access_token=access_token,
                    token_type="Bearer",
                    expires_in=core.config.JWT_TIMEOUT,
                    refresh_token=refresh_token_value,
                    scope=scope,
                ).model_dump(exclude_none=True)

                logger.info(f"准备返回token响应，数据键: {list(response_data.keys())}")

                return OAuthJSONResult(content=response_data, status_code=200)

            elif grant_type == "refresh_token":
                # 刷新令牌模式
                if not refresh_token:
                    return OAuthJSONResult(
                        content={"error": "invalid_request", "error_description": "缺少refresh_token"},
                        status_code=400,
                    )

                try:
                    header, payload = refresh_tokener.decode(refresh_token)
                    user_id = payload.get("user_id")
                except Exception as e:
                    return OAuthJSONResult(
                        content={"error": "invalid_grant", "error_description": "无效的refresh_token"},
                        status_code=400,
                    )

                # 生成新的access_token
                token_schema = TokenSchema(user_id=user_id)
                access_token = tokener.encode(**token_schema.model_dump())

                logger.info(f"刷新token: 客户端={client_id}, 用户={user_id}")

                # OAuth2.0标准要求直接返回JSON，不使用包装格式
                return OAuthJSONResult(
                    content=OAuthTokenResponse(
                        access_token=access_token,
                        token_type="Bearer",
                        expires_in=core.config.JWT_TIMEOUT,
                        refresh_token=refresh_token,  # 可以返回新的refresh_token或保持原样
                        scope=None,
                    ).model_dump(exclude_none=True),
                    status_code=200,
                )

            else:
                return OAuthJSONResult(
                    content={"error": "unsupported_grant_type", "error_description": f"不支持的grant_type: {grant_type}"},
                    status_code=400,
                )
        except Exception as e:
            # 捕获所有异常并记录日志
            logger.exception(f"Token端点异常: {str(e)}")
            return OAuthJSONResult(
                content={"error": "server_error", "error_description": f"服务器内部错误: {str(e)}"},
                status_code=500,
            )

    async def userinfo(self, token_schema: TokenSchema) -> OAuthJSONResult:
        """OAuth2.0用户信息端点：获取当前登录用户的信息。"""
        if not token_schema.user_id:
            raise exceptions.Http401UnauthorizedException(exceptions.Http401UnauthorizedException.TokenLost, "未登录")

        # 获取用户信息
        user = await self.user_repo.find_one(token_schema.user_id)

        if not user:
            raise exceptions.Http400BadRequestException(exceptions.Http400BadRequestException.NoResource, "用户不存在")

        user_schema = UserSchema.model_validate(user)

        return OAuthJSONResult(
            content=OAuthUserInfoResponse(
                user_id=str(user.id),
                user_name=user_schema.username,
            ).model_dump(exclude_none=True),
            status_code=200,
        )


async def get_oauth_service(db: AsyncSession = Depends(get_db)) -> OAuthService:
    return OAuthService(db)
