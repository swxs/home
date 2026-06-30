# -*- coding: utf-8 -*-
# @File    : repositories/wechat_msg_repository.py
# @AUTH    : code_creater

from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.wechat_msg import WechatMsg


class WechatMsgRepository(BaseRepository[WechatMsg]):
    """
    微信消息Repository
    可以在这里添加WechatMsg特定的查询方法
    """

    model = WechatMsg
    name = "wechat_msg"

    filterable_fields = {"msg_id", "msg_type", "msg_event", "msg"}
    sortable_fields = {"id", "create_at", "update_at", "msg_type", "msg_event"}

    # 如果需要WechatMsg特定的方法，可以在这里添加
