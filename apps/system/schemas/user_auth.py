# -*- coding: utf-8 -*-
# @FILE    : schemas/user_auth.py
# @AUTH    : model_creater

import datetime
from typing import Optional

from fastapi import Query

from web.custom_types import objectId
from web.schemas import BaseSchema

# 本模块方法
from .. import consts


# 说明：UserAuthSchema 作为字段基类保留，并被作为「创建/查询载荷」在 auth/oauth/wechat 等处复用。
class UserAuthSchema(BaseSchema):
    user_id: Optional[objectId] = None
    ttype: Optional[consts.UserAuth_Ttype] = None
    identifier: Optional[str] = None
    credential: Optional[str] = None
    ifverified: Optional[consts.UserAuth_Ifverified] = None


class UserAuthFilter(UserAuthSchema):
    """列表查询过滤条件。"""


class UserAuthCreate(UserAuthSchema):
    """创建入参。"""


class UserAuthUpdate(UserAuthSchema):
    """更新入参。"""


class UserAuthOut(UserAuthSchema):
    """输出 DTO。"""


async def get_user_auth_filter(
    user_id: Optional[str] = Query(None),
    ttype: Optional[int] = Query(None),
    identifier: Optional[str] = Query(None),
    credential: Optional[str] = Query(None),
    ifverified: Optional[int] = Query(None),
) -> UserAuthFilter:
    params = {}
    if user_id is not None:
        params["user_id"] = user_id
    if ttype is not None:
        params["ttype"] = ttype
    if identifier is not None:
        params["identifier"] = identifier
    if credential is not None:
        params["credential"] = credential
    if ifverified is not None:
        params["ifverified"] = ifverified

    return UserAuthFilter(**params)
