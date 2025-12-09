# -*- coding: utf-8 -*-
# @FILE    : schemas/password_lock.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, NotRequired, Optional, TypedDict

from fastapi import Query

from web.custom_types import objectId
from web.schemas import BaseSchema


class PasswordLockCustom(TypedDict):
    password: NotRequired[str]


class PasswordLockSchema(BaseSchema):
    user_id: Optional[objectId] = None
    name: Optional[str] = None
    key: Optional[str] = None
    website: Optional[str] = None
    used: Optional[int] = None
    ttype: Optional[int] = None
    custom: Optional[PasswordLockCustom] = None


async def get_password_lock_schema(
    user_id: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    key: Optional[str] = Query(None),
    website: Optional[str] = Query(None),
    used: Optional[str] = Query(None),
    ttype: Optional[str] = Query(None),
):
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

    return PasswordLockSchema(**params)
