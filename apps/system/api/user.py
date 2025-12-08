# -*- coding: utf-8 -*-
# @File    : api/user.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.token import TokenSchema, get_token
from web.exceptions import Http400BadRequestException
from web.response import success

# 本模块方法
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
    user_repo = UserRepository(db)

    # 使用Repository搜索方法
    result = await user_repo.search(user_schema, page_schema)

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
    user_repo = UserRepository(db)

    # 使用Repository查找方法
    user = await user_repo.find_one(user_id, "用户不存在")

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
    user_repo = UserRepository(db)

    # 使用Repository创建方法
    user = await user_repo.create_one(user_schema, "用户创建失败")

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
    user_repo = UserRepository(db)

    # 使用Repository更新方法
    user = await user_repo.update_one(
        user_id,
        user_schema,
        "用户不存在",
        "用户更新失败",
    )

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
    user_repo = UserRepository(db)

    # 使用Repository删除方法
    count = await user_repo.delete_one(user_id, "用户不存在", "用户删除失败")

    return success(
        {
            "count": count,
        }
    )
