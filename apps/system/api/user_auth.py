# -*- coding: utf-8 -*-
# @File    : api/user_auth.py
# @AUTH    : code_creater

import logging

from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.dependencies.pagination import get_pagination

# 本模块方法
from ..dao.user_auth import UserAuth
from ..schemas.user_auth import UserAuthSchema

router = APIRouter()

logger = logging.getLogger("main.apps.user_auth.api.user_auth")


@router.get("/{user_auth_id}")
async def get_user_auth(
    user_auth_id: str = Path(...),
):
    user_auth = await UserAuth.find(
        finds=user_auth_id,
    )
    return {
        "data": await user_auth.to_front(),
    }


@router.get("/")
async def get_user_auth_list(
    user_auth_schema=Query(...),
    pagination=Depends(get_pagination),
):
    user_auth_list = await UserAuth.search(
        searches=user_auth_schema.dict(exclude_unset=True),
        skip=pagination.skip,
        limit=pagination.limit,
    )
    return {
        "data": await user_auth_list.to_front(),
        "pagination": await user_auth_list.get_pagination(),
    }


@router.post("/")
async def create_user_auth(
    user_auth_schema: UserAuthSchema = Body(...),
):
    user_auth = await UserAuth.create(
        params=user_auth_schema.dict(),
    )
    return {
        "data": await user_auth.to_front(),
    }


@router.post("/{user_auth_id}")
async def copy_user_auth(
    user_auth_id: str = Path(...),
    user_auth_schema: UserAuthSchema = Body(...),
):
    user_auth = await UserAuth.copy(
        finds=user_auth_id,
        params=user_auth_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await user_auth.to_front(),
    }


@router.put("/{user_auth_id}")
async def change_user_auth(
    user_auth_id: str = Path(...),
    user_auth_schema: UserAuthSchema = Body(...),
):
    user_auth = await UserAuth.update(
        find=user_auth_id,
        params=user_auth_schema.dict(),
    )
    return {
        "data": await user_auth.to_front(),
    }


@router.delete("/{user_auth_id}")
async def delete_user_auth(
    user_auth_id: str = Path(...),
):
    count = await UserAuth.delete(
        find=user_auth_id,
    )
    return {
        "count": count,
    }


@router.patch("/{user_auth_id}")
async def modify_user_auth(
    user_auth_id: str = Path(...),
    user_auth_schema: UserAuthSchema = Body(...),
):
    user_auth = await UserAuth.update(
        find=user_auth_id,
        params=user_auth_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await user_auth.to_front(),
    }