# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..models.password_lock import PasswordLock
from ..repositories.password_lock_repository import PasswordLockRepository
from ..schemas.password_lock import PasswordLockSchema, get_password_lock_schema
from ..schemas.response import (
    CountResponse,
    PasswordLockResponse,
    PasswordLockSearchResponse,
)

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.password_lock")


@router.get("/", response_model=SuccessResponse[PasswordLockSearchResponse])
async def get_password_lock_list(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockSchema = Depends(get_password_lock_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, PasswordLock)
    async with single_worker as worker:
        result = await worker.repository.search(password_lock_schema, page_schema)

    return success(
        {
            "data": [PasswordLockSchema.model_validate(pl) for pl in result["data"]],
            "pagination": result["pagination"],
        }
    )


@router.get("/{password_lock_id}", response_model=SuccessResponse[PasswordLockResponse])
async def get_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, PasswordLock)
    async with single_worker as worker:
        password_lock = await worker.repository.find_one(password_lock_id)

    if password_lock is None:
        raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

    return success(
        {
            "data": PasswordLockSchema.model_validate(password_lock),
        }
    )


@router.post("/", response_model=SuccessResponse[PasswordLockResponse])
async def create_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, PasswordLock)
    async with single_worker as worker:
        password_lock = await worker.repository.create_one(password_lock_schema)

    return success(
        {
            "data": PasswordLockSchema.model_validate(password_lock),
        }
    )


@router.put("/{password_lock_id}", response_model=SuccessResponse[PasswordLockResponse])
async def modify_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    password_lock_schema: PasswordLockSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, PasswordLock)
    async with single_worker as worker:
        password_lock = await worker.repository.update_one(password_lock_id, password_lock_schema)

    return success(
        {
            "data": PasswordLockSchema.model_validate(password_lock),
        }
    )


@router.delete("/{password_lock_id}", response_model=SuccessResponse[CountResponse])
async def delete_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, PasswordLock)
    async with single_worker as worker:
        count = await worker.repository.delete_one(password_lock_id)

    return success(
        {
            "count": count,
        }
    )
