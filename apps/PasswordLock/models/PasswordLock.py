# -*- coding: utf-8 -*-
# @FILE    : models.py
# @AUTH    : model_creater

import bson
import datetime
from umongo import Document, fields

import core
from .. import consts


@core.mongodb_instance.register
class PasswordLock(Document):
    name = fields.StringField(allow_none=True)
    key = fields.StringField(allow_none=True)
    website = fields.StringField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)
    used = fields.IntField(allow_none=True, default=0)
    ttype = fields.IntField(
        allow_none=True, enums=consts.PASSWORD_LOCK_TTYPE_LIST, default=consts.PASSWORD_LOCK_TTYPE_COMMON
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
