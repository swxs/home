# -*- coding: utf-8 -*-
# @FILE    : schemas/user.py
# @AUTH    : model_creater

from typing import Dict, List, Optional
from bson import ObjectId
import pydantic


class UserSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    username: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[str] = None

    @pydantic.validator('avatar')
    def avatar_objectid(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        return ObjectId(v)
