# -*- coding: utf-8 -*-
# @FILE    : schemas/user_auth.py
# @AUTH    : model_creater

from typing import Dict, List, Optional
from bson import ObjectId
import pydantic


class UserAuthSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    user_id: Optional[str] = None
    ttype: Optional[int] = 0
    identifier: Optional[str] = None
    credential: Optional[str] = None
    ifverified: Optional[int] = 0

    @pydantic.validator('user_id')
    def user_id_objectid(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        return ObjectId(v)
