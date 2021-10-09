# -*- coding: utf-8 -*-
# @FILE    : models.py
# @AUTH    : model_creater

import bson
import datetime
from umongo import Document, fields

from core.db import instance
from ..consts import common_enum


@instance.register
class PasswordLock(Document):
    name = fields.StringField(allow_none=True)
    key = fields.StringField(allow_none=True)
    website = fields.StringField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)
    used = fields.IntField(allow_none=True, default=0)
    ttype = fields.IntField(
        allow_none=True, enums=common_enum.PASSWORD_LOCK_TTYPE_LIST, default=common_enum.PASSWORD_LOCK_TTYPE_COMMON
    )
    custom = fields.DictField(allow_none=True)
    created = fields.DateTimeField(allow_none=True, default=datetime.datetime.now)
    updated = fields.DateTimeField(allow_none=True, default=datetime.datetime.now)

    class Meta:
        indexes = [
            {
                'key': ['user_id, name'],
            },
        ]
        pass
