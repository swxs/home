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
    en = fields.StringField(
        requirement=False,
    )
    cn = fields.StringField(
        requirement=False,
    )
    number = fields.IntField(
        requirement=False,
        default=0,
    )
    last_time = fields.DateTimeField(
        requirement=False,
    )
    user_id = fields.ObjectIdField(
        requirement=False,
    )

    class Meta:
        indexes = [
            {
                'key': ['user_id'],
            },
        ]
        pass
