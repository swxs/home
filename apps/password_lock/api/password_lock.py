# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import logging

from bson import ObjectId
from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.response import success
from web.custom_types import OID
from web.dependencies.pagination import PageSchema, get_pagination

# 本模块方法
from ..dao.password_lock import PasswordLock
from ..schemas.password_lock import PasswordLockSchema, get_password_lock_schema

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.password_lock")


@router.get("/")
async def get_password_lock_list(
    password_lock_schema: PasswordLockSchema = Depends(get_password_lock_schema),
    pagination: PageSchema = Depends(get_pagination),
):
    password_lock_list = await PasswordLock.search(
        searches=password_lock_schema.dict(exclude_unset=True),
        skip=pagination.skip,
        limit=pagination.limit,
    )
    return success(
        {
            "data": await password_lock_list.to_dict(),
        }
    )


@router.get("/{password_lock_id}")
async def get_password_lock(
    password_lock_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    password_lock = await PasswordLock.find_one(
        finds={"id": ObjectId(password_lock_id)},
    )
    return success(
        {
            "data": password_lock,
        }
    )


@router.post("/")
async def create_password_lock(
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.create(
        params=password_lock_schema.dict(),
    )
    return success(
        {
            "data": password_lock,
        }
    )


@router.put("/{password_lock_id}")
async def modify_password_lock(
    password_lock_id: OID = Path(..., regex="[0-9a-f]{24}"),
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.update_one(
        finds={"id": ObjectId(password_lock_id)},
        params=password_lock_schema.dict(exclude_defaults=True),
    )
    return success(
        {
            "data": password_lock,
        }
    )


@router.delete("/{password_lock_id}")
async def delete_password_lock(
    password_lock_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    count = await PasswordLock.delete_one(
        finds={"id": ObjectId(password_lock_id)},
    )
    return success(
        {
            "count": count,
        }
    )
