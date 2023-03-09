# -*- coding: utf-8 -*-
# @FILE    : models/word.py
# @AUTH    : code_creater

from umongo import Document, fields

import core


@core.mongodb_instance.register
class Word(Document):
    en = fields.StringField(
        required=False,
        unique=False,
        allow_none=False,
    )
    cn = fields.StringField(
        required=False,
        unique=False,
        allow_none=False,
    )
    number = fields.IntField(
        required=False,
        unique=False,
        allow_none=False,
    )
    last_time = fields.DateTimeField(
        required=False,
        unique=False,
        allow_none=False,
    )
    user_id = fields.ObjectIdField(
        required=False,
        unique=False,
        allow_none=False,
    )

    class Meta:
        indexes = [
            {
                'key': ['user_id'],
            },
        ]
        pass
