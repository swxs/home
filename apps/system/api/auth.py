# -*- coding: utf-8 -*-
# @File    : api/auth.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, BackgroundTasks, Body, Query
from fastapi.param_functions import Depends
from fastapi.responses import RedirectResponse

from web.response import success
from web.schemas.response import SuccessResponse

# 本模块方法
from ..schemas.auth import (
    ForgotPasswordRequest,
    MessageResponse,
    RegisterRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from ..schemas.response import TokenResponse, UserAuthResponse
from ..schemas.user_auth import UserAuthSchema
from ..services.auth_service import AuthService, get_auth_service

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.auth")


@router.post("/refresh_token", response_model=SuccessResponse[TokenResponse])
async def get_refresh_token(
    ttype: int = Body(..., embed=True),
    identifier: str = Body(..., embed=True),
    credential: str = Body(..., embed=True),
    service: AuthService = Depends(get_auth_service),
):
    result = await service.refresh_token(ttype, identifier, credential)
    return success(result)


@router.post("/token", response_model=SuccessResponse[TokenResponse])
async def refresh_access_token(
    refresh_token: str = Body(..., embed=True),
    service: AuthService = Depends(get_auth_service),
):
    result = await service.token(refresh_token)
    return success(result)


@router.post("/signin", response_model=SuccessResponse[UserAuthResponse])
async def signin(
    user_auth_schema: UserAuthSchema = Body(...),
    service: AuthService = Depends(get_auth_service),
):
    user_auth = await service.signin(user_auth_schema)
    return success({"data": user_auth})


@router.post("/register", response_model=SuccessResponse[MessageResponse])
async def register(
    body: RegisterRequest,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.register(body.username, body.email, body.password, background_tasks)
    return success(result)


@router.post("/verify-email", response_model=SuccessResponse[MessageResponse])
async def verify_email(
    body: VerifyEmailRequest = Body(...),
    service: AuthService = Depends(get_auth_service),
):
    result = await service.verify_email(body.token)
    return success(result)


@router.post("/resend-verification", response_model=SuccessResponse[MessageResponse])
async def resend_verification(
    body: ResendVerificationRequest,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.resend_verification(body.email, background_tasks)
    return success(result)


@router.post("/forgot-password", response_model=SuccessResponse[MessageResponse])
async def forgot_password(
    body: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(get_auth_service),
):
    result = await service.forgot_password(body.username, body.email, background_tasks)
    return success(result)


@router.post("/reset-password", response_model=SuccessResponse[MessageResponse])
async def reset_password(
    body: ResetPasswordRequest = Body(...),
    service: AuthService = Depends(get_auth_service),
):
    result = await service.reset_password(body.token, body.new_password)
    return success(result)


@router.get("/github/login")
async def github_login(
    service: AuthService = Depends(get_auth_service),
):
    """
    GitHub OAuth登录入口，重定向到GitHub授权页面
    """
    result = await service.github_login()
    return success(result)


@router.get("/github/callback")
async def github_callback(
    code: str = Query(...),
    state: str = Query(None),
    service: AuthService = Depends(get_auth_service),
):
    """
    GitHub OAuth回调处理
    """
    redirect_url = await service.github_callback(code, state)
    return RedirectResponse(url=redirect_url)
