# -*- coding: utf-8 -*-
# @File    : api/oauth.py
# @AUTH    : code_creater

import logging
from typing import Optional

from fastapi import APIRouter, Form, Query, Request
from fastapi.param_functions import Depends

from web.response import CORSResponse
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 通用方法
from commons.Helpers import tokener

# 本模块方法
from ..schemas.oauth import OAuthUserInfoResponse
from ..services.oauth_service import OAuthService, get_oauth_service

oauth_router = APIRouter(prefix="/oauth", tags=["oauth"])

logger = logging.getLogger("main.apps.system.api.oauth")


@oauth_router.options("/{path:path}")
async def options_handler(path: str, request: Request = None):
    """处理 CORS 预检请求"""
    # 返回 204 No Content，这是 OPTIONS 预检请求的标准响应
    response = CORSResponse(status_code=204)
    return response


def _resolve_user_id_from_request(request: Request) -> Optional[str]:
    """从请求中解析 user_id（三通道：Bearer Header / Cookie / Query）。"""
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

    return user_id


@oauth_router.get("/authorize")
async def authorize(
    client_id: str = Query(...),
    redirect_uri: str = Query(...),
    response_type: str = Query(default="code"),
    scope: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    confirm: Optional[str] = Query(None),  # 用户确认授权
    request: Request = None,
    service: OAuthService = Depends(get_oauth_service),
):
    """
    OAuth2.0授权端点

    处理客户端的授权请求，生成授权码并重定向到客户端
    """
    # 检查用户登录状态（通过token或cookie），三通道解析保留在 api 层
    user_id = _resolve_user_id_from_request(request)

    return await service.authorize(
        client_id=client_id,
        redirect_uri=redirect_uri,
        response_type=response_type,
        scope=scope,
        state=state,
        confirm=confirm,
        user_id=user_id,
    )


@oauth_router.post("/token")
async def token(
    grant_type: str = Form(...),
    code: Optional[str] = Form(None),
    redirect_uri: Optional[str] = Form(None),
    client_id: str = Form(...),
    client_secret: str = Form(...),
    refresh_token: Optional[str] = Form(None),
    service: OAuthService = Depends(get_oauth_service),
):
    """
    OAuth2.0令牌端点

    用授权码换取访问令牌，或使用refresh_token刷新令牌
    """
    return await service.token(
        grant_type=grant_type,
        code=code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
        refresh_token=refresh_token,
    )


@oauth_router.get("/userinfo", response_model=SuccessResponse[OAuthUserInfoResponse])
async def userinfo(
    token_schema: TokenSchema = Depends(get_token),
    service: OAuthService = Depends(get_oauth_service),
):
    """
    OAuth2.0用户信息端点

    获取当前登录用户的信息
    """
    return await service.userinfo(token_schema)
