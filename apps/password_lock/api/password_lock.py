# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import logging

from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.dependencies.token import TokenSchema, get_token
from web.dependencies.pagination import PageSchema, get_pagination

# 本模块方法
from ..dao.password_lock import PasswordLock
from ..schemas.password_lock import PasswordLockSchema

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.password_lock")


@router.get("/{password_lock_id}", response_model=PasswordLockSchema)
async def get_password_lock(
    token=Depends(get_token),
    password_lock_id: str = Path(...),
):
    password_lock = await PasswordLock.find_one(
        finds={
            "id": password_lock_id,
        }
    )
    return password_lock


@router.get("/")
async def get_password_lock_list(
    token: TokenSchema = Depends(get_token),
    pagination: PageSchema = Depends(get_pagination),
):
    password_lock_list = await PasswordLock.search(
        searches={"user_id": token.user_id},
        limit=pagination.limit,
        skip=pagination.skip,
    )
    return {
        "data": password_lock_list,
    }


@router.post("/", response_model=PasswordLockSchema)
async def create_password_lock(
    token=Depends(get_token),
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock_schema.user_id = token.user_id
    password_lock = await PasswordLock.create(
        params=password_lock_schema.dict(),
    )
    return password_lock


@router.put("/{password_lock_id}", response_model=PasswordLockSchema)
async def change_password_lock(
    token=Depends(get_token),
    password_lock_id: str = Path(...),
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.update_one(
        finds={"id": password_lock_id},
        params=password_lock_schema.dict(exclude_defaults=True),
    )
    return password_lock


@router.delete("/{password_lock_id}", response_model=PasswordLockSchema)
async def delete_password_lock(
    token=Depends(get_token),
    password_lock_id: str = Path(...),
):
    count = await PasswordLock.delete_one(
        finds={"id": password_lock_id},
    )
    return count


@router.patch("/{password_lock_id}", response_model=PasswordLockSchema)
async def modify_password_lock(
    token=Depends(get_token),
    password_lock_id: str = Path(...),
    password_lock_schema: PasswordLockSchema = Body(...),
):
    password_lock = await PasswordLock.update_one(
        finds={"id": password_lock_id},
        params=password_lock_schema.dict(exclude_defaults=True),
    )
    return password_lock
