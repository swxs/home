# -*- coding: utf-8 -*-
# @FILE    : schemas/wechat_msg.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, Optional

import pydantic
from bson import ObjectId
from fastapi import Query

from web.custom_types import OID


class WechatMsgSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    msg_id: Optional[str] = None
    msg_type: Optional[str] = None
    msg_event: Optional[str] = None
    msg: Optional[str] = None


async def get_wechat_msg_schema(
    msg_id: Optional[str] = Query(None),
    msg_type: Optional[str] = Query(None),
    msg_event: Optional[str] = Query(None),
    msg: Optional[str] = Query(None),
):
    params = {}
    if msg_id is not None:
        params["msg_id"] = msg_id
    if msg_type is not None:
        params["msg_type"] = msg_type
    if msg_event is not None:
        params["msg_event"] = msg_event
    if msg is not None:
        params["msg"] = msg

    return WechatMsgSchema(**params)
