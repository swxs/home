# -*- coding: utf-8 -*-
# @File    : api/user.py
# @AUTH    : code_creater

import logging

from bson import ObjectId
from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.response import success
from web.custom_types import OID
from web.dependencies.token import TokenSchema, get_token
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination

# 本模块方法
from ..dao.user import User
from ..schemas.user import UserSchema, get_user_schema

router = APIRouter()

logger = logging.getLogger("main.apps.user.api.user")


@router.get("/")
async def get_user_list(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserSchema = Depends(get_user_schema),
    page_schema: PageSchema = Depends(get_pagination),
):
    user_list = (
        await User.search(
            searches=user_schema.dict(exclude_unset=True),
            skip=page_schema.skip,
            limit=page_schema.limit,
        )
    ).order_by(page_schema.order_by)

    pagination = PaginationSchema(
        total=await User.count(
            finds=user_schema.dict(exclude_unset=True),
        ),
        order_by=page_schema.order_by,
        use_pager=page_schema.use_pager,
        page=page_schema.page,
        page_number=page_schema.page_number,
    )

    return success(
        {
            "data": await user_list.to_dict(),
            "pagination": pagination.dict(),
        }
    )


@router.get("/{user_id}")
async def get_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    user = await User.find_one(
        finds={"id": ObjectId(user_id)},
    )

    return success(
        {
            "data": user,
        }
    )


@router.post("/")
async def create_user(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserSchema = Body(...),
):
    user = await User.create(
        params=user_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": user,
        }
    )


@router.put("/{user_id}")
async def modify_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: OID = Path(..., regex="[0-9a-f]{24}"),
    user_schema: UserSchema = Body(...),
):
    user = await User.update_one(
        finds={"id": ObjectId(user_id)},
        params=user_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": user,
        }
    )


@router.delete("/{user_id}")
async def delete_user(
    token_schema: TokenSchema = Depends(get_token),
    user_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    count = await User.delete_one(
        finds={"id": ObjectId(user_id)},
    )

    return success(
        {
            "count": count,
        }
    )
