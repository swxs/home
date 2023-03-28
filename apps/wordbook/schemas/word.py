# -*- coding: utf-8 -*-
# @FILE    : schemas/word.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, Optional

import pydantic
from bson import ObjectId
from fastapi import Query

from web.custom_types import OID


class WordSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    en: Optional[str] = None
    cn: Optional[str] = None
    number: Optional[int] = None
    last_time: Optional[datetime.datetime] = None
    user_id: Optional[OID] = None


async def get_word_schema(
    en: Optional[str] = Query(None),
    cn: Optional[str] = Query(None),
    number: Optional[str] = Query(None),
    last_time: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
):
    params = {}
    if en is not None:
        params["en"] = en
    if cn is not None:
        params["cn"] = cn
    if number is not None:
        params["number"] = number
    if last_time is not None:
        params["last_time"] = last_time
    if user_id is not None:
        params["user_id"] = user_id

    return WordSchema(**params)
