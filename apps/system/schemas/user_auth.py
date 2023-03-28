# -*- coding: utf-8 -*-
# @FILE    : schemas/user_auth.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, Optional

import pydantic
from bson import ObjectId
from fastapi import Query

from web.custom_types import OID


class UserAuthSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    user_id: Optional[OID] = None
    ttype: Optional[int] = None
    identifier: Optional[str] = None
    credential: Optional[str] = None
    ifverified: Optional[int] = None


async def get_user_auth_schema(
    user_id: Optional[str] = Query(None),
    ttype: Optional[str] = Query(None),
    identifier: Optional[str] = Query(None),
    credential: Optional[str] = Query(None),
    ifverified: Optional[str] = Query(None),
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
