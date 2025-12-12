# -*- coding: utf-8 -*-
# @File    : api/user.py
# @AUTH    : code_creater

import logging

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
from ..models.user import User
from ..schemas.response import CountResponse, UserResponse, UserSearchResponse
from ..schemas.user import UserSchema, get_user_schema

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.user")


@router.get("/", response_model=SuccessResponse[UserSearchResponse])
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
    return success(
        {
            "data": [UserSchema.model_validate(user) for user in result["data"]],
            "pagination": result["pagination"],
        }
    )


@router.get("/{user_id}", response_model=SuccessResponse[UserResponse])
async def get_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        user = await worker.repository.find_one(user_id)

    if user is None:
        raise Http400BadRequestException(Http400BadRequestException.NoResource, "用户不存在")

    # 转换为 Schema
    return success(
        {
            "data": UserSchema.model_validate(user),
        }
    )


@router.post("/", response_model=SuccessResponse[UserResponse])
async def create_user(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        user = await worker.repository.create_one(user_schema)

    return success(
        {
            "data": UserSchema.model_validate(user),
        }
    )


@router.put("/{user_id}", response_model=SuccessResponse[UserResponse])
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
    return success(
        {
            "data": UserSchema.model_validate(user),
        }
    )


@router.delete("/{user_id}", response_model=SuccessResponse[CountResponse])
async def delete_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, User)
    async with single_worker as worker:
        count = await worker.repository.delete_one(user_id)

    return success(
        {
            "count": count,
        }
    )
