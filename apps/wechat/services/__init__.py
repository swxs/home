# -*- coding: utf-8 -*-
# @File    : services/__init__.py
# @AUTH    : code_creater

# 本模块方法
from .wechat_message_service import (
    WechatMessageService,
    get_wechat_message_service,
)
from .wechat_msg_service import WechatMsgService, get_wechat_msg_service

__all__ = [
    "WechatMessageService",
    "get_wechat_message_service",
    "WechatMsgService",
    "get_wechat_msg_service",
]
