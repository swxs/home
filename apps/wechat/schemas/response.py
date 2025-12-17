# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import Dict, List, TypedDict

from web.schemas.pagination import PaginationSchema

# 本模块方法
from .wechat_msg import WechatMsgSchema


class WechatMsgSearchResponse(TypedDict):
    data: List[WechatMsgSchema]
    pagination: PaginationSchema


class WechatMsgResponse(TypedDict):
    data: WechatMsgSchema


class WechatMsgTestResponse(TypedDict):
    reply: str
