# -*- coding: utf-8 -*-
# @FILE    : schemas/wechat_msg.py
# @AUTH    : model_creater

import datetime
from typing import Dict, List, Optional

import pydantic
from bson import ObjectId
from fastapi import Body, Query

from web.custom_types import OID


class WechatMsgTestSchema(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed = True

    msg: Optional[str] = None


async def get_wechat_msg_test_schema(
    msg: Optional[str] = Query(None),
):
    params = {}
    if msg is not None:
        params["msg"] = msg

    return WechatMsgTestSchema(**params)
