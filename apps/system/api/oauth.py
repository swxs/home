# -*- coding: utf-8 -*-
# @File    : api/oauth.py
# @AUTH    : code_creater

import logging
from datetime import datetime
from typing import Optional
from urllib.parse import urlencode

from fastapi import APIRouter, Form, Header, Query, Request
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import core
from web import exceptions
from web.dependencies.db import get_db, get_single_worker, get_unit_worker
from web.dependencies.unit_worker import UnitWorker
from web.response import (
    CORSJSONResponse,
    CORSRedirectResponse,
    CORSResponse,
)
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 通用方法
from commons.Helpers import refresh_tokener, tokener

# 本模块方法
from ..models.oauth_authorization_code import OAuthAuthorizationCode
from ..models.oauth_client import OAuthClient
from ..models.user import User
from ..repositories.oauth_authorization_code_repository import (
    OAuthAuthorizationCodeRepository,
)
from ..repositories.oauth_client_repository import OAuthClientRepository
from ..repositories.user_repository import UserRepository
from ..schemas.oauth import OAuthTokenRequest, OAuthTokenResponse, OAuthUserInfoResponse
from ..schemas.oauth_authorization_code import (
    OAuthAuthorizationCodeSchema,
)
from ..schemas.oauth_client import OAuthClientSchema
from ..schemas.user import UserSchema
from ..utils.oauth import (
    build_authorization_url,
    build_error_redirect_url,
    generate_authorization_code,
    get_authorization_code_expires_at,
    validate_redirect_uri,
)

oauth_router = APIRouter(prefix="/oauth", tags=["oauth"])

logger = logging.getLogger("main.apps.system.api.oauth")


@oauth_router.options("/{path:path}")
async def options_handler(path: str, request: Request = None):
    """处理 CORS 预检请求"""
    # 返回 204 No Content，这是 OPTIONS 预检请求的标准响应
    response = CORSResponse(status_code=204)
    return response


@oauth_router.get("/authorize")
async def authorize(
    client_id: str = Query(...),
    redirect_uri: str = Query(...),
    response_type: str = Query(default="code"),
    scope: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    confirm: Optional[str] = Query(None),  # 用户确认授权
    request: Request = None,
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth2.0授权端点

    处理客户端的授权请求，生成授权码并重定向到客户端
    """
    # 验证response_type
    if response_type != "code":
        if redirect_uri:
            error_url = build_error_redirect_url(
                redirect_uri, "unsupported_response_type", f"不支持的response_type: {response_type}", state
            )
            return CORSRedirectResponse(url=error_url)
        raise exceptions.Http400BadRequestException(
            exceptions.Http400BadRequestException.InvalidParameter, f"不支持的response_type: {response_type}"
        )

    # 验证客户端
    single_worker = await get_single_worker(db, OAuthClient)
    async with single_worker as worker:
        oauth_client = await worker.repository.find_one_or_none(OAuthClientSchema(client_id=client_id))

    if not oauth_client:
        if redirect_uri:
            error_url = build_error_redirect_url(redirect_uri, "invalid_client", "无效的客户端ID", state)
            return CORSRedirectResponse(url=error_url)
        raise exceptions.Http400BadRequestException(
            exceptions.Http400BadRequestException.InvalidParameter, "无效的客户端ID"
        )

    # 验证客户端是否激活
    if oauth_client.is_active != 1:  # 1表示ACTIVE
        if redirect_uri:
            error_url = build_error_redirect_url(redirect_uri, "invalid_client", "客户端未激活", state)
            return CORSRedirectResponse(url=error_url)
        raise exceptions.Http400BadRequestException(
            exceptions.Http400BadRequestException.InvalidParameter, "客户端未激活"
        )

    # 验证redirect_uri
    if not validate_redirect_uri(oauth_client.redirect_uri, redirect_uri):
        if redirect_uri:
            error_url = build_error_redirect_url(redirect_uri, "invalid_request", "重定向URI不匹配", state)
            return CORSRedirectResponse(url=error_url)
        raise exceptions.Http400BadRequestException(
            exceptions.Http400BadRequestException.InvalidParameter, "重定向URI不匹配"
        )

    # 检查用户登录状态（通过token或cookie）
    # 注意：这里需要从请求中获取token，可以通过多种方式：
    # 1. Authorization header (Bearer token)
    # 2. Cookie中的token
    # 3. 查询参数中的token（不推荐，但某些场景可能需要）
    user_id = None

    # 方式1: 从Authorization header获取
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        try:
            header, payload = tokener.decode(token)
            user_id = payload.get("user_id")
        except Exception:
            pass

    # 方式2: 从Cookie获取（如果前端设置了cookie）
    if not user_id:
        token_cookie = request.cookies.get("access_token")
        if token_cookie:
            try:
                header, payload = tokener.decode(token_cookie)
                user_id = payload.get("user_id")
            except Exception:
                pass

    # 方式3: 从查询参数获取（用于从登录页面重定向回来时）
    if not user_id:
        token_param = request.query_params.get("token")
        if token_param:
            try:
                header, payload = tokener.decode(token_param)
                user_id = payload.get("user_id")
            except Exception:
                pass

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
        return CORSRedirectResponse(url=f"{login_url}{separator}{urlencode(params)}")

    # 如果用户已登录但未确认，且confirm参数不为true，重定向到授权确认页面
    if confirm != "true":
        # 这里可以重定向到授权确认页面，当前实现直接生成授权码
        # 如果需要授权确认页面，可以重定向到openapi_auth的/authorize页面
        pass

    # 生成授权码
    code = generate_authorization_code()
    expires_at = get_authorization_code_expires_at()

    # 保存授权码到数据库
    unit_worker = await get_unit_worker(db)
    async with unit_worker as uw:
        auth_code_repo: OAuthAuthorizationCodeRepository = uw.get_repository(OAuthAuthorizationCode)

        auth_code_schema = {
            "code": code,
            "client_id": client_id,
            "user_id": user_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "expires_at": expires_at,
            "is_used": False,
        }

        auth_code = await auth_code_repo.create_one(OAuthAuthorizationCodeSchema(**auth_code_schema))

    logger.info(f"生成授权码: {code}, 客户端: {client_id}, 用户: {user_id}")

    # 重定向到客户端，带上授权码
    redirect_url = build_authorization_url(redirect_uri, code, state)
    return CORSRedirectResponse(url=redirect_url)


@oauth_router.post("/token")
async def token(
    grant_type: str = Form(...),
    code: Optional[str] = Form(None),
    redirect_uri: Optional[str] = Form(None),
    client_id: str = Form(...),
    client_secret: str = Form(...),
    refresh_token: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth2.0令牌端点

    用授权码换取访问令牌，或使用refresh_token刷新令牌
    """
    try:
        logger.info(f"Token请求开始: grant_type={grant_type}, client_id={client_id}")

        # 验证客户端
        single_worker = await get_single_worker(db, OAuthClient)
        async with single_worker as worker:
            oauth_client = await worker.repository.find_one_or_none(OAuthClientSchema(client_id=client_id))

        if not oauth_client:
            # OAuth2.0标准错误响应格式
            return CORSJSONResponse(
                content={"error": "invalid_client", "error_description": "无效的客户端ID"},
                status_code=400,
            )

        # 验证客户端密钥
        if oauth_client.client_secret != client_secret:
            return CORSJSONResponse(
                content={"error": "invalid_client", "error_description": "无效的客户端密钥"},
                status_code=400,
            )

        # 验证客户端是否激活
        if oauth_client.is_active != 1:
            return CORSJSONResponse(
                content={"error": "invalid_client", "error_description": "客户端未激活"},
                status_code=400,
            )

        if grant_type == "authorization_code":
            # 授权码模式
            if not code or not redirect_uri:
                return CORSJSONResponse(
                    content={"error": "invalid_request", "error_description": "缺少必要的参数"},
                    status_code=400,
                )

            # 查找授权码
            unit_worker = await get_unit_worker(db)
            auth_code = None
            user_id = None
            scope = None

            async with unit_worker as uw:
                auth_code_repo: OAuthAuthorizationCodeRepository = uw.get_repository(OAuthAuthorizationCode)

                auth_code = await auth_code_repo.find_one_or_none(OAuthAuthorizationCodeSchema(code=code))

            if not auth_code:
                logger.warning(f"授权码不存在: {code}")
                return CORSJSONResponse(
                    content={"error": "invalid_grant", "error_description": "无效的授权码"},
                    status_code=400,
                )

            # 验证授权码是否已使用
            if auth_code.is_used:
                logger.warning(f"授权码已使用: {code}")
                return CORSJSONResponse(
                    content={"error": "invalid_grant", "error_description": "授权码已使用"},
                    status_code=400,
                )

            if auth_code.expires_at < datetime.utcnow():
                logger.warning(f"授权码已过期: {code}, 过期时间: {auth_code.expires_at}")
                return CORSJSONResponse(
                    content={"error": "invalid_grant", "error_description": "授权码已过期"},
                    status_code=400,
                )

            # 验证授权码是否属于该客户端
            if auth_code.client_id != client_id:
                logger.warning(
                    f"授权码与客户端不匹配: code={code}, code_client={auth_code.client_id}, request_client={client_id}"
                )
                return CORSJSONResponse(
                    content={"error": "invalid_grant", "error_description": "授权码与客户端不匹配"},
                    status_code=400,
                )

            # 验证redirect_uri是否匹配
            if not validate_redirect_uri(auth_code.redirect_uri, redirect_uri):
                logger.warning(f"重定向URI不匹配: code_uri={auth_code.redirect_uri}, request_uri={redirect_uri}")
                return CORSJSONResponse(
                    content={"error": "invalid_request", "error_description": "重定向URI不匹配"},
                    status_code=400,
                )

            # 标记授权码为已使用（在单独的事务中）
            async with unit_worker as uw:
                auth_code_repo: OAuthAuthorizationCodeRepository = uw.get_repository(OAuthAuthorizationCode)

                await auth_code_repo.update_one(str(auth_code.id), OAuthAuthorizationCodeSchema(is_used=True))
                # 提交事务
                await uw.commit()

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

            # 使用带 CORS 的 JSONResponse，确保响应能正确返回
            logger.info(f"CORSJSONResponse已创建，准备返回")
            return CORSJSONResponse(
                content=response_data,
                status_code=200,
            )

        elif grant_type == "refresh_token":
            # 刷新令牌模式
            if not refresh_token:
                return CORSJSONResponse(
                    content={"error": "invalid_request", "error_description": "缺少refresh_token"},
                    status_code=400,
                )

            try:
                header, payload = refresh_tokener.decode(refresh_token)
                user_id = payload.get("user_id")
            except Exception as e:
                return CORSJSONResponse(
                    content={"error": "invalid_grant", "error_description": "无效的refresh_token"},
                    status_code=400,
                )

            # 生成新的access_token
            token_schema = TokenSchema(user_id=user_id)
            access_token = tokener.encode(**token_schema.model_dump())

            logger.info(f"刷新token: 客户端={client_id}, 用户={user_id}")

            # OAuth2.0标准要求直接返回JSON，不使用包装格式
            return CORSJSONResponse(
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
            return CORSJSONResponse(
                content={"error": "unsupported_grant_type", "error_description": f"不支持的grant_type: {grant_type}"},
                status_code=400,
            )
    except Exception as e:
        # 捕获所有异常并记录日志
        logger.exception(f"Token端点异常: {str(e)}")
        return CORSJSONResponse(
            content={"error": "server_error", "error_description": f"服务器内部错误: {str(e)}"},
            status_code=500,
        )


@oauth_router.get("/userinfo", response_model=SuccessResponse[OAuthUserInfoResponse])
async def userinfo(
    token_schema: TokenSchema = Depends(get_token),
    db: AsyncSession = Depends(get_db),
):
    """
    OAuth2.0用户信息端点

    获取当前登录用户的信息
    """
    if not token_schema.user_id:
        raise exceptions.Http401UnauthorizedException(exceptions.Http401UnauthorizedException.TokenLost, "未登录")

    # 获取用户信息
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        user = await worker.repository.find_one(token_schema.user_id)

    if not user:
        raise exceptions.Http400BadRequestException(exceptions.Http400BadRequestException.NoResource, "用户不存在")

    user_schema = UserSchema.model_validate(user)

    return CORSJSONResponse(
        content=OAuthUserInfoResponse(
            user_id=str(user.id),
            user_name=user_schema.username,
        ).model_dump(exclude_none=True),
        status_code=200,
    )
