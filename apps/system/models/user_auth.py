# -*- coding: utf-8 -*-
# @FILE    : models/user_auth.py
# @AUTH    : code_creater

from umongo import Document, fields

import core


@core.mongodb_instance.register
class UserAuth(Document):
    created = fields.DateTimeField(
        required=True,
        unique=False,
        allow_none=False,
    )
    updated = fields.DateTimeField(
        required=True,
        unique=False,
        allow_none=False,
    )
    user_id = fields.ObjectIdField(
        required=True,
        unique=False,
        allow_none=False,
    )
    ttype = fields.IntField(
        required=True,
        unique=False,
        allow_none=False,
    )
    identifier = fields.StringField(
        required=True,
        unique=False,
        allow_none=False,
    )
    credential = fields.StringField(
        required=False,
        unique=False,
        allow_none=False,
    )
    ifverified = fields.IntField(
        required=False,
        unique=False,
        allow_none=False,
    )

    class Meta:
        indexes = [
            {
                'key': ['user_id'],
            },
            {
                'key': ['ttype, identifier'],
            },
        ]
        pass
