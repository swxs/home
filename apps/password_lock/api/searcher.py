# -*- coding: utf-8 -*-
# @File    : api/searcher.py
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
from web.schemas.search import SearchSchema, get_search
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from .. import password_lock_utils
from ..models.password_lock import PasswordLock
from ..schemas.password_lock import PasswordLockSchema, get_password_lock_schema
from ..schemas.response import PasswordLockSearchResponse, PasswordResponse

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.searcher")


@router.get("/self", response_model=SuccessResponse[PasswordLockSearchResponse])
async def get_password_lock_list(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockSchema = Depends(get_password_lock_schema),
    search_schema: SearchSchema = Depends(get_search),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    # 设置用户ID过滤
    password_lock_schema.user_id = token_schema.user_id

    single_worker = await get_single_worker(db, PasswordLock)
    async with single_worker as worker:
        # 使用Repository搜索方法（支持名称模糊搜索）
        result = await worker.repository.search_with_name_like(
            password_lock_schema,
            page_schema,
            name_search=search_schema.search if search_schema.search else None,
        )

    return success(
        {
            "data": [PasswordLockSchema.model_validate(pl) for pl in result["data"]],
            "pagination": result["pagination"],
        }
    )


@router.get("/self/{password_lock_id}", response_model=SuccessResponse[PasswordResponse])
async def get_password(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, PasswordLock)
    async with single_worker as worker:
        # 使用Repository查找方法
        password_lock = await worker.repository.find_one(password_lock_id)

        if password_lock is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

        if str(password_lock.user_id) != token_schema.user_id:
            raise Http400BadRequestException(Http400BadRequestException.IllegalArgument, "无权访问该密码")

        await worker.repository.update_one(password_lock_id, PasswordLockSchema(used=password_lock.used + 1))

    # 获取密码
    password_lock_schema = PasswordLockSchema.model_validate(password_lock)
    password = await password_lock_utils.get_password(password_lock_schema)

    return success(
        {
            "password": password,
        }
    )
