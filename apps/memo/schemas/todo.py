# -*- coding: utf-8 -*-
# @FILE    : schemas/todo.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, Optional

import pydantic
from bson import ObjectId
from fastapi import Query

from web.custom_types import OID


class TodoSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    user_id: Optional[OID] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    document: Optional[str] = None
    status: Optional[int] = None
    priority: Optional[int] = None


async def get_todo_schema(
    user_id: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    summary: Optional[str] = Query(None),
    document: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
):
    params = {}
    if user_id is not None:
        params["user_id"] = user_id
    if title is not None:
        params["title"] = title
    if summary is not None:
        params["summary"] = summary
    if document is not None:
        params["document"] = document
    if status is not None:
        params["status"] = status
    if priority is not None:
        params["priority"] = priority

    return TodoSchema(**params)
