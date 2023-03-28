# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import logging

from bson import ObjectId
from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.response import success
from web.custom_types import OID
from web.dependencies.token import TokenSchema, get_token
from web.dependencies.pagination import PageSchema, get_pagination

# 本模块方法
from .. import password_lock_utils
from ..dao.password_lock import PasswordLock
from ..schemas.password_lock import PasswordLockSchema, get_password_lock_schema

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.password_lock")


@router.get("/self")
async def get_password_lock_list(
    token_schema: TokenSchema = Depends(get_token),
    password_lock_schema: PasswordLockSchema = Depends(get_password_lock_schema),
    pagination: PageSchema = Depends(get_pagination),
):
    searches = {}
    searches.update(token_schema.dict(exclude_unset=True))
    searches.update(password_lock_schema.dict(exclude_unset=True))

    password_lock_list = await PasswordLock.search(
        searches=searches,
        skip=pagination.skip,
        limit=pagination.limit,
    )

    result_list = []
    async for password_lock in password_lock_list:
        result_list.append(await password_lock_utils.to_front(password_lock))

    return success(
        {
            "data": result_list,
        }
    )
