# -*- coding: utf-8 -*-
# @FILE    : schemas/todo.py
# @AUTH    : model_creater

from typing import Dict, List, Optional
from bson import ObjectId
import pydantic


class TodoSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    title: Optional[str] = None
    summary: Optional[str] = None
    document: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[int] = 0
    priority: Optional[int] = 0
    user_id: Optional[str] = None

    @pydantic.validator('user_id')
    def user_id_objectid(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        return ObjectId(v)

    @pydantic.validator('user_id')
    def user_id_objectid(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        return ObjectId(v)
