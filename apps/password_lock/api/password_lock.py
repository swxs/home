# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
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
from ..repositories.password_lock_repository import PasswordLockRepository
from ..schemas.password_lock import PasswordLockSchema, get_password_lock_schema

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.password_lock")


@router.get("/")
async def get_password_lock_list(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockSchema = Depends(get_password_lock_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    password_lock_repo = PasswordLockRepository(db)

    # 使用Repository搜索方法
    result = await password_lock_repo.search(password_lock_schema, page_schema)

    # 转换为 Schema
    password_lock_list = [PasswordLockSchema.model_validate(pl).model_dump() for pl in result["data"]]

    return success(
        {
            "data": password_lock_list,
            "pagination": result["pagination"].model_dump(),
        }
    )


@router.get("/{password_lock_id}")
async def get_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    password_lock_repo = PasswordLockRepository(db)

    # 使用Repository查找方法
    password_lock = await password_lock_repo.find_one(password_lock_id, "密码锁不存在")

    # 转换为 Schema
    password_lock_response = PasswordLockSchema.model_validate(password_lock)

    return success(
        {
            "data": password_lock_response.model_dump(),
        }
    )


@router.post("/")
async def create_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    password_lock_repo = PasswordLockRepository(db)

    # 使用Repository创建方法
    password_lock = await password_lock_repo.create_one(password_lock_schema, "密码锁创建失败")

    password_lock_response = PasswordLockSchema.model_validate(password_lock)

    return success(
        {
            "data": password_lock_response.model_dump(),
        }
    )


@router.put("/{password_lock_id}")
async def modify_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    password_lock_schema: PasswordLockSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    password_lock_repo = PasswordLockRepository(db)

    # 使用Repository更新方法
    password_lock = await password_lock_repo.update_one(
        password_lock_id,
        password_lock_schema,
        "密码锁不存在",
        "密码锁更新失败",
    )

    # 转换为 Schema
    password_lock_response = PasswordLockSchema.model_validate(password_lock)

    return success(
        {
            "data": password_lock_response.model_dump(),
        }
    )


@router.delete("/{password_lock_id}")
async def delete_password_lock(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    password_lock_repo = PasswordLockRepository(db)

    # 使用Repository删除方法
    count = await password_lock_repo.delete_one(password_lock_id, "密码锁不存在", "密码锁删除失败")

    return success(
        {
            "count": count,
        }
    )
