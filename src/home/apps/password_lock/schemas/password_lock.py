# -*- coding: utf-8 -*-
# @FILE    : schemas/password_lock.py
# @AUTH    : model_creater

from typing import NotRequired, Optional, TypedDict

from fastapi import Query

from home.web.schemas.types import objectId
from home.web.schemas import BaseSchema


class PasswordLockCustom(TypedDict):
    password: NotRequired[str]


class _PasswordLockFields(BaseSchema):
    """密码锁字段集合，供各用途 schema 复用。"""

    user_id: Optional[objectId] = None
    name: Optional[str] = None
    key: Optional[str] = None
    website: Optional[str] = None
    used: Optional[int] = None
    ttype: Optional[int] = None
    custom: Optional[PasswordLockCustom] = None


class PasswordLockFilter(_PasswordLockFields):
    """列表查询过滤条件。"""


class PasswordLockCreate(_PasswordLockFields):
    """创建入参。"""


class PasswordLockUpdate(_PasswordLockFields):
    """更新入参。"""


class PasswordLockOut(_PasswordLockFields):
    """输出 DTO。"""


async def get_password_lock_filter(
    user_id: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    key: Optional[str] = Query(None),
    website: Optional[str] = Query(None),
    used: Optional[str] = Query(None),
    ttype: Optional[str] = Query(None),
) -> PasswordLockFilter:
    params = {}
    if user_id is not None:
        params["user_id"] = user_id
    if name is not None:
        params["name"] = name
    if key is not None:
        params["key"] = key
    if website is not None:
        params["website"] = website
    if used is not None:
        params["used"] = used
    if ttype is not None:
        params["ttype"] = ttype

    return PasswordLockFilter(**params)
