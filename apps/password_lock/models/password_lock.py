# -*- coding: utf-8 -*-
# @FILE    : models/password_lock.py
# @AUTH    : code_creater

from umongo import Document, fields

import core


@core.mongodb_instance.register
class PasswordLock(Document):
    created = fields.DateTimeField(
        required=True,
        allow_none=False,
    )
    updated = fields.DateTimeField(
        required=True,
        allow_none=False,
    )
    user_id = fields.ObjectIdField(
        required=True,
        allow_none=False,
    )
    name = fields.StringField(
        required=True,
        allow_none=False,
    )
    key = fields.StringField(
        required=True,
        allow_none=False,
    )
    website = fields.StringField(
        required=False,
        allow_none=True,
    )
    used = fields.IntField(
        required=False,
        allow_none=False,
    )
    ttype = fields.IntField(
        required=True,
        allow_none=False,
    )
    custom = fields.DictField(
        required=False,
        allow_none=False,
    )

    class Meta:
        indexes = [
            {
                'key': ['user_id', 'name'],
                'unique': True,
            },
        ]
        pass
