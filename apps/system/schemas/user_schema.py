# -*- coding: utf-8 -*-
# @FILE    : schemas/user.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, Optional

import pydantic
from bson import ObjectId
from fastapi import Query

from web.custom_types import OID


class UserSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    username: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[OID] = None


async def get_user_schema(
    username: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    avatar: Optional[str] = Query(None),
):
    params = {}
    if username is not None:
        params["username"] = username
    if description is not None:
        params["description"] = description
    if avatar is not None:
        params["avatar"] = avatar

    return UserSchema(**params)
