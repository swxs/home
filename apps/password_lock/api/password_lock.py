# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import logging

from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.dependencies.pagination import get_pagination

# 本模块方法
from ..dao.password_lock import PasswordLock
from ..schemas.password_lock import PasswordLockSchema

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.password_lock")


@router.get("/{password_lock_id}")
async def get_password_lock(
    password_lock_id: str = Path(...),
):
    password_lock = await PasswordLock.find(
        finds=password_lock_id,
    )
    return {
        "data": await password_lock.to_front(),
    }


@router.get("/")
async def get_password_lock_list(
    password_lock_schema=Query(...),
    pagination=Depends(get_pagination),
):
    password_lock_list = await PasswordLock.search(
        searches=password_lock_schema.dict(exclude_unset=True),
        skip=pagination.skip,
        limit=pagination.limit,
    )
    return {
        "data": await password_lock_list.to_front(),
        "pagination": await password_lock_list.get_pagination(),
    }


@router.post("/")
async def create_password_lock(
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.create(
        params=password_lock_schema.dict(),
    )
    return {
        "data": await password_lock.to_front(),
    }


@router.post("/{password_lock_id}")
async def copy_password_lock(
    password_lock_id: str = Path(...),
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.copy(
        finds=password_lock_id,
        params=password_lock_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await password_lock.to_front(),
    }


@router.put("/{password_lock_id}")
async def change_password_lock(
    password_lock_id: str = Path(...),
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.update(
        find=password_lock_id,
        params=password_lock_schema.dict(),
    )
    return {
        "data": await password_lock.to_front(),
    }


@router.delete("/{password_lock_id}")
async def delete_password_lock(
    password_lock_id: str = Path(...),
):
    count = await PasswordLock.delete(
        find=password_lock_id,
    )
    return {
        "count": count,
    }


@router.patch("/{password_lock_id}")
async def modify_password_lock(
    password_lock_id: str = Path(...),
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.update(
        find=password_lock_id,
        params=password_lock_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await password_lock.to_front(),
    }
