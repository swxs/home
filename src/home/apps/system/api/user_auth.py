# -*- coding: utf-8 -*-
# @File    : api/user_auth.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.pagination import PageSchema, get_pagination
from home.web.schemas.response import CountResponse, SuccessResponse
from home.web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.response import UserAuthResponse, UserAuthSearchResponse
from ..schemas.user_auth import (
    UserAuthCreate,
    UserAuthFilter,
    UserAuthUpdate,
    get_user_auth_filter,
)
from ..services.user_auth_service import UserAuthService, get_user_auth_service

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.user_auth")


@router.get("/", response_model=SuccessResponse[UserAuthSearchResponse])
async def get_user_auth_list(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_schema: UserAuthFilter = Depends(get_user_auth_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: UserAuthService = Depends(get_user_auth_service),
):
    result = await service.list(user_auth_schema, page_schema)
    return success(result)


@router.get("/{user_auth_id}", response_model=SuccessResponse[UserAuthResponse])
async def get_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: UserAuthService = Depends(get_user_auth_service),
):
    user_auth = await service.get(user_auth_id)
    return success({"data": user_auth})


@router.post("/", response_model=SuccessResponse[UserAuthResponse])
async def create_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_schema: UserAuthCreate = Body(...),
    service: UserAuthService = Depends(get_user_auth_service),
):
    user_auth = await service.create(user_auth_schema)
    return success({"data": user_auth})


@router.put("/{user_auth_id}", response_model=SuccessResponse[UserAuthResponse])
async def modify_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    user_auth_schema: UserAuthUpdate = Body(...),
    service: UserAuthService = Depends(get_user_auth_service),
):
    user_auth = await service.update(user_auth_id, user_auth_schema)
    return success({"data": user_auth})


@router.delete("/{user_auth_id}", response_model=SuccessResponse[CountResponse])
async def delete_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: UserAuthService = Depends(get_user_auth_service),
):
    count = await service.delete(user_auth_id)
    return success({"count": count})
