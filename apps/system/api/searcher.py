# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
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
from .. import user_utils
from ..dao.user import User
from ..dao.user_auth import UserAuth
from ..schemas.user import UserSchema, get_user_schema

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.searcher")


@router.get("/self")
async def get_user_with_user_auth_list(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserSchema = Depends(get_user_schema),
    page_schema: PageSchema = Depends(get_pagination),
):
    searches = {}
    searches.update(user_schema.dict(exclude_unset=True))

    user_list = (
        await User.search(
            searches=searches,
            skip=page_schema.skip,
            limit=page_schema.limit,
        )
    ).order_by(page_schema.order_by)

    user_data_list = [user.to_dict() async for user in user_list]

    user_auth_list = await UserAuth.search(
        searches={"user_id": {"$in": [ObjectId(user_data.id) for user_data in user_data_list]}},
    )
    infos = {str(user_auth.user_id): {"user_auth": user_auth.to_dict()} async for user_auth in user_auth_list}

    [user_data.update(infos.get(user_data.id, {})) for user_data in user_data_list]

    pagination = PaginationSchema(
        total=await User.count(
            finds=searches,
        ),
        order_by=page_schema.order_by,
        use_pager=page_schema.use_pager,
        page=page_schema.page,
        page_number=page_schema.page_number,
    )

    return success(
        {
            "data": user_data_list,
            "pagination": pagination.dict(),
        }
    )
