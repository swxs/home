# -*- coding: utf-8 -*-
# @File    : api/user_auth.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.token import TokenSchema, get_token
from web.exceptions import Http400BadRequestException
from web.response import success

# 本模块方法
from ..models.user_auth import UserAuth
from ..repositories.user_auth_repository import UserAuthRepository
from ..schemas.user_auth import UserAuthSchema, get_user_auth_schema

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.user_auth")


@router.get("/")
async def get_user_auth_list(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_schema: UserAuthSchema = Depends(get_user_auth_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, UserAuth)
    async with single_worker as worker:
        result = await worker.repository.search(user_auth_schema, page_schema)

    # 转换为 Schema
    user_auth_list = [UserAuthSchema.model_validate(user_auth).model_dump() for user_auth in result["data"]]

    return success(
        {
            "data": user_auth_list,
            "pagination": result["pagination"].model_dump(),
        }
    )


@router.get("/{user_auth_id}")
async def get_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, UserAuth)
    async with single_worker as worker:
        user_auth = await worker.repository.find_one(user_auth_id)

    # 转换为 Schema
    user_auth_response = UserAuthSchema.model_validate(user_auth)

    return success(
        {
            "data": user_auth_response.model_dump(),
        }
    )


@router.post("/")
async def create_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_schema: UserAuthSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, UserAuth)
    async with single_worker as worker:
        user_auth = await worker.repository.create_one(user_auth_schema)

    user_auth_response = UserAuthSchema.model_validate(user_auth)

    return success(
        {
            "data": user_auth_response.model_dump(),
        }
    )


@router.put("/{user_auth_id}")
async def modify_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    user_auth_schema: UserAuthSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, UserAuth)
    async with single_worker as worker:
        user_auth = await worker.repository.update_one(user_auth_id, user_auth_schema)

    # 转换为 Schema
    user_auth_response = UserAuthSchema.model_validate(user_auth)

    return success(
        {
            "data": user_auth_response.model_dump(),
        }
    )


@router.delete("/{user_auth_id}")
async def delete_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, UserAuth)
    async with single_worker as worker:
        count = await worker.repository.delete_one(user_auth_id)

    return success(
        {
            "count": count,
        }
    )
