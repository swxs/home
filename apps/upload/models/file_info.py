# -*- coding: utf-8 -*-
# @FILE    : models/file_info.py
# @AUTH    : code_creater

from umongo import Document, fields

import core


@core.mongodb_instance.register
class FileInfo(Document):
    created = fields.DateTimeField(
        required=True,
        allow_none=False,
    )
    updated = fields.DateTimeField(
        required=True,
        allow_none=False,
    )
    file_id = fields.StringField(
        required=True,
        allow_none=False,
    )
    file_name = fields.StringField(
        required=True,
        allow_none=False,
    )
    file_size = fields.IntField(
        required=False,
        allow_none=False,
    )
    ext = fields.StringField(
        required=False,
        allow_none=True,
    )
    policy = fields.IntField(
        required=True,
        allow_none=False,
    )

    class Meta:
        indexes = [
            {
                'key': ['file_id'],
                'unique': True,
            },
        ]
        pass
