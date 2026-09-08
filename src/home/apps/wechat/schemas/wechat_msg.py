# -*- coding: utf-8 -*-
# @FILE    : schemas/wechat_msg.py
# @AUTH    : model_creater

from typing import Optional

from fastapi import Query

from home.web.schemas import BaseSchema


class _WechatMsgFields(BaseSchema):
    """微信消息字段集合，供各用途 schema 复用。"""

    msg_id: Optional[str] = None
    msg_type: Optional[str] = None
    msg_event: Optional[str] = None
    msg: Optional[str] = None


class WechatMsgFilter(_WechatMsgFields):
    """列表查询过滤条件。"""


class WechatMsgCreate(_WechatMsgFields):
    """创建入参。"""


class WechatMsgUpdate(_WechatMsgFields):
    """更新入参。"""


class WechatMsgOut(_WechatMsgFields):
    """输出 DTO。"""


async def get_wechat_msg_filter(
    msg_id: Optional[str] = Query(None),
    msg_type: Optional[str] = Query(None),
    msg_event: Optional[str] = Query(None),
    msg: Optional[str] = Query(None),
) -> WechatMsgFilter:
    params = {}
    if msg_id is not None:
        params["msg_id"] = msg_id
    if msg_type is not None:
        params["msg_type"] = msg_type
    if msg_event is not None:
        params["msg_event"] = msg_event
    if msg is not None:
        params["msg"] = msg

    return WechatMsgFilter(**params)
