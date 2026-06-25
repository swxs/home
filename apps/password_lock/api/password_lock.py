# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path
from fastapi.param_functions import Depends

from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import CountResponse, SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.password_lock import (
    PasswordLockCreate,
    PasswordLockFilter,
    PasswordLockUpdate,
    get_password_lock_filter,
)
from ..schemas.response import (
    PasswordLockResponse,
    PasswordLockSearchResponse,
)
from ..services.password_lock_service import (
    PasswordLockService,
    get_password_lock_service,
)

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.password_lock")


@router.get("/", response_model=SuccessResponse[PasswordLockSearchResponse])
async def get_password_lock_list(
    token_schema: TokenSchema = Depends(get_token),
    filter_schema: PasswordLockFilter = Depends(get_password_lock_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: PasswordLockService = Depends(get_password_lock_service),
):
    result = await service.list(filter_schema, page_schema)
    return success(result)


@router.get("/{password_lock_id}", response_model=SuccessResponse[PasswordLockResponse])
async def get_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: PasswordLockService = Depends(get_password_lock_service),
):
    password_lock = await service.get(password_lock_id)
    return success({"data": password_lock})


@router.post("/", response_model=SuccessResponse[PasswordLockResponse])
async def create_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockCreate = Body(...),
    service: PasswordLockService = Depends(get_password_lock_service),
):
    password_lock = await service.create(password_lock_schema)
    return success({"data": password_lock})


@router.put("/{password_lock_id}", response_model=SuccessResponse[PasswordLockResponse])
async def modify_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    password_lock_schema: PasswordLockUpdate = Body(...),
    service: PasswordLockService = Depends(get_password_lock_service),
):
    password_lock = await service.update(password_lock_id, password_lock_schema)
    return success({"data": password_lock})


@router.delete("/{password_lock_id}", response_model=SuccessResponse[CountResponse])
async def delete_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: PasswordLockService = Depends(get_password_lock_service),
):
    count = await service.delete(password_lock_id)
    return success({"count": count})
