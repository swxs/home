# -*- coding: utf-8 -*-
# @FILE    : models/todo.py
# @AUTH    : code_creater

from umongo import Document, fields

import core


@core.mongodb_instance.register
class Todo(Document):
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
    title = fields.StringField(
        required=True,
        unique=False,
        allow_none=False,
    )
    summary = fields.StringField(
        required=False,
        unique=False,
        allow_none=False,
    )
    document = fields.StringField(
        required=False,
        unique=False,
        allow_none=False,
    )
    status = fields.IntField(
        required=False,
        unique=False,
        allow_none=False,
    )
    priority = fields.IntField(
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
