# -*- coding: utf-8 -*-
# @File    : dao/wechat_msg.py
# @AUTH    : code_creater

import logging
import datetime

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.wechat_msg import WechatMsg as WechatMsgModel

logger = logging.getLogger("main.apps.wechat.dao.wechat_msg")


class WechatMsg(BaseDocument):
    id = fields.PrimaryField()
    created = fields.DateTimeField(
        default_create=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        default_create=datetime.datetime.now,
        default_update=datetime.datetime.now,
    )
    msg_id = fields.StringField()
    msg_type = fields.StringField()
    msg_event = fields.StringField()
    msg = fields.StringField()

    class Meta:
        model = WechatMsgModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(WechatMsg, self).__init__(**kwargs)
