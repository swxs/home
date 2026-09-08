# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import Dict, List, TypedDict

from home.web.schemas.pagination import PaginationSchema

# 本模块方法
from .wechat_msg import WechatMsgOut


class WechatMsgSearchResponse(TypedDict):
    data: List[WechatMsgOut]
    pagination: PaginationSchema


class WechatMsgResponse(TypedDict):
    data: WechatMsgOut


class WechatMsgTestResponse(TypedDict):
    reply: str
