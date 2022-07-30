# -*- coding: utf-8 -*-
# @FILE    : schemas/password_lock.py
# @AUTH    : model_creater

from typing import Dict, List, Optional
from bson import ObjectId
import pydantic


class PasswordLockSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: Optional[str] = None
    key: Optional[str] = None
    website: Optional[str] = None
    user_id: Optional[str] = None
    used: Optional[int] = 0
    ttype: Optional[int] = 0
    custom: Optional[Dict] = None

    @pydantic.validator('user_id')
    def user_id_objectid(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        return ObjectId(v)
