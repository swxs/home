# -*- coding: utf-8 -*-
# @File    : api/user.py
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
from ..models.user import User
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserSchema, get_user_schema

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.user")


@router.get("/")
async def get_user_list(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserSchema = Depends(get_user_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        result = await worker.repository.search(user_schema, page_schema)

    # 转换为 Schema
    user_list = [UserSchema.model_validate(user).model_dump() for user in result["data"]]

    return success(
        {
            "data": user_list,
            "pagination": result["pagination"].model_dump(),
        }
    )


@router.get("/{user_id}")
async def get_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        user = await worker.repository.find_one(user_id)

    # 转换为 Schema
    user_response = UserSchema.model_validate(user)

    return success(
        {
            "data": user_response.model_dump(),
        }
    )


@router.post("/")
async def create_user(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        user = await worker.repository.create_one(user_schema)

    user_response = UserSchema.model_validate(user)

    return success(
        {
            "data": user_response.model_dump(),
        }
    )


@router.put("/{user_id}")
async def modify_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    user_schema: UserSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        user = await worker.repository.update_one(user_id, user_schema)

    # 转换为 Schema
    user_response = UserSchema.model_validate(user)

    return success(
        {
            "data": user_response.model_dump(),
        }
    )


@router.delete("/{user_id}")
async def delete_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        await worker.repository.delete_one(user_id)

    return success(
        {
            "count": 1,
        }
    )
