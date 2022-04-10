# -*- coding: utf-8 -*-
# @File    : api/user.py
# @AUTH    : code_creater

import logging

from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.dependencies.pagination import get_pagination

# 本模块方法
from ..dao.user import User
from ..schemas.user import UserSchema

router = APIRouter()

logger = logging.getLogger("main.apps.user.api.user")


@router.get("/{user_id}")
async def get_user(
    user_id: str = Path(...),
):
    user = await User.find(
        finds=user_id,
    )
    return {
        "data": await user.to_front(),
    }


@router.get("/")
async def get_user_list(
    user_schema=Query(...),
    pagination=Depends(get_pagination),
):
    user_list = await User.search(
        searches=user_schema.dict(exclude_unset=True),
        skip=pagination.skip,
        limit=pagination.limit,
    )
    return {
        "data": await user_list.to_front(),
        "pagination": await user_list.get_pagination(),
    }


@router.post("/")
async def create_user(
    user_schema: UserSchema = Body(...),
):
    user = await User.create(
        params=user_schema.dict(),
    )
    return {
        "data": await user.to_front(),
    }


@router.post("/{user_id}")
async def copy_user(
    user_id: str = Path(...),
    user_schema: UserSchema = Body(...),
):
    user = await User.copy(
        finds=user_id,
        params=user_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await user.to_front(),
    }


@router.put("/{user_id}")
async def change_user(
    user_id: str = Path(...),
    user_schema: UserSchema = Body(...),
):
    user = await User.update(
        find=user_id,
        params=user_schema.dict(),
    )
    return {
        "data": await user.to_front(),
    }


@router.delete("/{user_id}")
async def delete_user(
    user_id: str = Path(...),
):
    count = await User.delete(
        find=user_id,
    )
    return {
        "count": count,
    }


@router.patch("/{user_id}")
async def modify_user(
    user_id: str = Path(...),
    user_schema: UserSchema = Body(...),
):
    user = await User.update(
        find=user_id,
        params=user_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await user.to_front(),
    }
