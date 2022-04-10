# -*- coding: utf-8 -*-
# @FILE    : models/word.py
# @AUTH    : code_creater

import datetime

import bson
from umongo import Document, fields

import core

# 本模块方法
from .. import consts


@core.mongodb_instance.register
class Word(Document):
    en = fields.StringField(allow_none=True)
    cn = fields.StringField(allow_none=True)
    number = fields.IntField(allow_none=True, default=0)
    last_time = fields.DateTimeField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['user_id'],
            },
        ]
        pass
