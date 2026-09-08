# -*- coding: utf-8 -*-
# @FILE    : schemas/user.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, Optional

import pydantic
from bson import ObjectId
from fastapi import Query

from home.web.schemas.types import objectId
from home.web.schemas import BaseSchema


# 说明：UserSchema 作为字段基类保留，并被作为「创建/查询载荷」在 auth/oauth/wechat 等处复用。
class UserSchema(BaseSchema):
    username: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[objectId] = None


class UserFilter(UserSchema):
    """列表查询过滤条件。"""


class UserCreate(UserSchema):
    """创建入参。"""


class UserUpdate(UserSchema):
    """更新入参。"""


class UserOut(UserSchema):
    """输出 DTO。"""


async def get_user_filter(
    username: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    avatar: Optional[objectId] = Query(None),
) -> UserFilter:
    params = {}
    if username is not None:
        params["username"] = username
    if description is not None:
        params["description"] = description
    if avatar is not None:
        params["avatar"] = avatar

    return UserFilter(**params)
