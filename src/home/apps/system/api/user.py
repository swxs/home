# -*- coding: utf-8 -*-
# @File    : api/user.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.pagination import PageSchema, get_pagination
from home.web.schemas.response import CountResponse, SuccessResponse
from home.web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.response import UserResponse, UserSearchResponse
from ..schemas.user import UserCreate, UserFilter, UserUpdate, get_user_filter
from ..services.user_service import UserService, get_user_service

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.user")


@router.get("/", response_model=SuccessResponse[UserSearchResponse])
async def get_user_list(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserFilter = Depends(get_user_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: UserService = Depends(get_user_service),
):
    result = await service.list(user_schema, page_schema)
    return success(result)


@router.get("/{user_id}", response_model=SuccessResponse[UserResponse])
async def get_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: UserService = Depends(get_user_service),
):
    user = await service.get(user_id)
    return success({"data": user})


@router.post("/", response_model=SuccessResponse[UserResponse])
async def create_user(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserCreate = Body(...),
    service: UserService = Depends(get_user_service),
):
    user = await service.create(user_schema)
    return success({"data": user})


@router.put("/{user_id}", response_model=SuccessResponse[UserResponse])
async def modify_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    user_schema: UserUpdate = Body(...),
    service: UserService = Depends(get_user_service),
):
    user = await service.update(user_id, user_schema)
    return success({"data": user})


@router.delete("/{user_id}", response_model=SuccessResponse[CountResponse])
async def delete_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: UserService = Depends(get_user_service),
):
    count = await service.delete(user_id)
    return success({"count": count})
