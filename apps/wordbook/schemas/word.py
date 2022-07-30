# -*- coding: utf-8 -*-
# @FILE    : schemas/word.py
# @AUTH    : model_creater

from typing import Dict, List, Optional
from bson import ObjectId
import pydantic


class WordSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    en: Optional[str] = None
    cn: Optional[str] = None
    number: Optional[int] = 0
    last_time: Optional[datetime] = None
    user_id: Optional[str] = None

    @pydantic.validator('user_id')
    def user_id_objectid(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        return ObjectId(v)
