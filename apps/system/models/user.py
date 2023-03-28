# -*- coding: utf-8 -*-
# @FILE    : models/user.py
# @AUTH    : code_creater

from umongo import Document, fields

import core


@core.mongodb_instance.register
class User(Document):
    created = fields.DateTimeField(
        required=True,
        allow_none=False,
    )
    updated = fields.DateTimeField(
        required=True,
        allow_none=False,
    )
    username = fields.StringField(
        required=True,
        allow_none=False,
    )
    description = fields.StringField(
        required=False,
        allow_none=True,
    )
    avatar = fields.ObjectIdField(
        required=False,
        allow_none=True,
    )

    class Meta:
        indexes = [
            {
                'key': ['username'],
                'unique': True,
            },
        ]
        pass
