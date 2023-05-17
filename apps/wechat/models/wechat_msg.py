# -*- coding: utf-8 -*-
# @FILE    : models/wechat_msg.py
# @AUTH    : code_creater

from umongo import Document, fields

import core


@core.mongodb_instance.register
class WechatMsg(Document):
    created = fields.DateTimeField(
        required=True,
        allow_none=False,
    )
    updated = fields.DateTimeField(
        required=True,
        allow_none=False,
    )
    msg_id = fields.StringField(
        required=False,
        allow_none=False,
    )
    msg_type = fields.StringField(
        required=False,
        allow_none=False,
    )
    msg_event = fields.StringField(
        required=False,
        allow_none=False,
    )
    msg = fields.StringField(
        required=False,
        allow_none=False,
    )

    class Meta:
        indexes = [
            {
                'key': ['msg_id'],
                'sparse': True,
                'unique': True,
            },
        ]
        pass
