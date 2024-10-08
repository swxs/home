# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import logging
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends

from web.custom_types import OID
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.search import SearchSchema, get_search
from web.dependencies.token import TokenSchema, get_token
from web.response import success

# 本模块方法
from .. import password_lock_utils
from ..dao.password_lock import PasswordLock
from ..schemas.password_lock import PasswordLockSchema, get_password_lock_schema

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.searcher")


@router.get("/self")
async def get_password_lock_list(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockSchema = Depends(get_password_lock_schema),
    search_schema: SearchSchema = Depends(get_search),
    page_schema: PageSchema = Depends(get_pagination),
):
    searches: dict[str, Any] = {
        "user_id": ObjectId(token_schema.user_id),
    }
    searches.update(password_lock_schema.dict(exclude_unset=True))
    if search_schema.search:
        searches.update({"name": {"$regex": search_schema.search}})

    password_lock_list = (
        await PasswordLock.search(
            searches=searches,
            skip=page_schema.skip,
            limit=page_schema.limit,
        )
    ).order_by(page_schema.order_by)

    pagination = PaginationSchema(
        total=await PasswordLock.count(
            finds=searches,
        ),
        order_by=page_schema.order_by,
        use_pager=page_schema.use_pager,
        page=page_schema.page,
        page_number=page_schema.page_number,
    )

    return success(
        {
            "data": await password_lock_list.to_dict(),
            "pagination": pagination.dict(),
        }
    )


@router.get('/self/{password_lock_id}')
async def get_password(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    password_lock = await PasswordLock.find_one(
        finds={
            "user_id": ObjectId(token_schema.user_id),
            "id": ObjectId(password_lock_id),
        },
        nullable=False,
    )

    return success(
        {
            "password": await password_lock_utils.get_password(password_lock),
        }
    )
