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


class UserAuthSchema(BaseSchema):
    user_id: Optional[objectId] = None
    ttype: Optional[consts.UserAuth_Ttype] = None
    identifier: Optional[str] = None
    credential: Optional[str] = None
    ifverified: Optional[consts.UserAuth_Ifverified] = None


async def get_user_auth_schema(
    user_id: Optional[str] = Query(None),
    ttype: Optional[int] = Query(None),
    identifier: Optional[str] = Query(None),
    credential: Optional[str] = Query(None),
    ifverified: Optional[int] = Query(None),
):
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

    return UserAuthSchema(**params)
