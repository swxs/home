# -*- coding: utf-8 -*-
# @FILE    : schemas/file_info.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, Optional

import pydantic
from bson import ObjectId
from fastapi import Query

from web.custom_types import OID


class FileInfoSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    file_id: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    ext: Optional[str] = None
    policy: Optional[int] = None


async def get_file_info_schema(
    file_id: Optional[str] = Query(None),
    file_name: Optional[str] = Query(None),
    file_size: Optional[str] = Query(None),
    ext: Optional[str] = Query(None),
    policy: Optional[str] = Query(None),
):
    params = {}
    if file_id is not None:
        params["file_id"] = file_id
    if file_name is not None:
        params["file_name"] = file_name
    if file_size is not None:
        params["file_size"] = file_size
    if ext is not None:
        params["ext"] = ext
    if policy is not None:
        params["policy"] = policy

    return FileInfoSchema(**params)
