# -*- coding: utf-8 -*-
# @File    : api/searcher.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.search import SearchSchema, get_search
from web.dependencies.token import TokenSchema, get_token
from web.exceptions import Http400BadRequestException
from web.response import success

# 本模块方法
from .. import password_lock_utils
from ..repositories.password_lock_repository import PasswordLockRepository
from ..schemas.password_lock import PasswordLockSchema, get_password_lock_schema

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.searcher")


@router.get("/self")
async def get_password_lock_list(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockSchema = Depends(get_password_lock_schema),
    search_schema: SearchSchema = Depends(get_search),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    password_lock_repo = PasswordLockRepository(db)

    # 设置用户ID过滤
    password_lock_schema.user_id = token_schema.user_id

    # 使用Repository搜索方法（支持名称模糊搜索）
    result = await password_lock_repo.search_with_name_like(
        password_lock_schema,
        page_schema,
        name_search=search_schema.search if search_schema.search else None,
    )

    # 转换为 Schema
    password_lock_list = [PasswordLockSchema.model_validate(pl).model_dump() for pl in result["data"]]

    return success(
        {
            "data": password_lock_list,
            "pagination": result["pagination"].model_dump(),
        }
    )


@router.get("/self/{password_lock_id}")
async def get_password(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    password_lock_repo = PasswordLockRepository(db)

    # 使用Repository查找方法
    password_lock = await password_lock_repo.find_one(password_lock_id, "密码锁不存在")

    # 验证用户权限
    if str(password_lock.user_id) != token_schema.user_id:
        raise Http400BadRequestException(Http400BadRequestException.NoResource, "无权访问该密码锁")

    # 获取密码
    password = await password_lock_utils.get_password(password_lock)

    return success(
        {
            "password": password,
        }
    )
