# -*- coding: utf-8 -*-
# @File    : views.py
# @AUTH    : model

import logging
from fastapi import APIRouter, Path, Query, Body
from fastapi.param_functions import Depends

from web.dependencies.pagination import get_pagination
from ..schemas.password_lock import PasswordLockSchema
from ..dao.password_lock import PasswordLock
from ..utils import password_lock_utils


router = APIRouter()

logger = logging.getLogger("main.password_lock.api.password_lock")


@router.get("/{password_lock_id}")
async def get_passwordlock(
    password_lock_id: str = Path(...),
):
    password_lock = await PasswordLock.find(
        finds=password_lock_id,
    )
    return {
        "data": await password_lock.to_front(),
    }


@router.get("/")
async def get_passwordlock_list(
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


@router.post("/{passwordlock_id}")
async def copy_passwordlock(
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


@router.post("/")
async def create_passwordlock(
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.create(
        params=password_lock_schema.dict(),
    )
    try:
        ls = await password_lock.to_front()
    except Exception as e:
        print(e)
    return {
        "data": await password_lock.to_front(),
    }


@router.put("/{passwordlock_id}")
async def change_passwordlock(
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


@router.delete("/{passwordlock_id}")
async def delete_passwordlick(
    password_lock_id: str = Path(...),
):
    count = await PasswordLock.delete(
        find=password_lock_id,
    )
    return {
        "count": count,
    }


@router.patch("/{passwordlock_id}")
async def modify_passwordlick(
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
