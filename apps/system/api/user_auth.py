# -*- coding: utf-8 -*-
# @File    : api/user_auth.py
# @AUTH    : code_creater

import logging

from bson import ObjectId
from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends

from web.custom_types import OID
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.token import TokenSchema, get_token
from web.response import success

# 本模块方法
from ..dao.user_auth import UserAuth
from ..schemas.user_auth import UserAuthSchema, get_user_auth_schema

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.user_auth")


@router.get("/")
async def get_user_auth_list(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_schema: UserAuthSchema = Depends(get_user_auth_schema),
    page_schema: PageSchema = Depends(get_pagination),
):
    user_auth_list = (
        await UserAuth.search(
            searches=user_auth_schema.dict(exclude_unset=True),
            skip=page_schema.skip,
            limit=page_schema.limit,
        )
    ).order_by(page_schema.order_by)

    pagination = PaginationSchema(
        total=await UserAuth.count(
            finds=user_auth_schema.dict(exclude_unset=True),
        ),
        order_by=page_schema.order_by,
        use_pager=page_schema.use_pager,
        page=page_schema.page,
        page_number=page_schema.page_number,
    )

    return success(
        {
            "data": await user_auth_list.to_dict(),
            "pagination": pagination.dict(),
        }
    )


@router.get("/{user_auth_id}")
async def get_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    user_auth = await UserAuth.find_one(
        finds={"id": ObjectId(user_auth_id)},
        nullable=False,
    )

    return success(
        {
            "data": user_auth,
        }
    )


@router.post("/")
async def create_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_schema: UserAuthSchema = Body(...),
):
    user_auth = await UserAuth.create(
        params=user_auth_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": user_auth,
        }
    )


@router.put("/{user_auth_id}")
async def modify_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: OID = Path(..., regex="[0-9a-f]{24}"),
    user_auth_schema: UserAuthSchema = Body(...),
):
    user_auth = await UserAuth.update_one(
        finds={"id": ObjectId(user_auth_id)},
        params=user_auth_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": user_auth,
        }
    )


@router.delete("/{user_auth_id}")
async def delete_user_auth(
    token_schema: TokenSchema = Depends(get_token),
    user_auth_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    count = await UserAuth.delete_one(
        finds={"id": ObjectId(user_auth_id)},
    )

    return success(
        {
            "count": count,
        }
    )
