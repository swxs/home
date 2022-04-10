# -*- coding: utf-8 -*-
# @FILE    : models/todo.py
# @AUTH    : code_creater

import datetime

import bson
from umongo import Document, fields

import core

# 本模块方法
from .. import consts


@core.mongodb_instance.register
class Todo(Document):
    title = fields.StringField(allow_none=True)
    summary = fields.StringField(allow_none=True)
    document = fields.StringField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)
    status = fields.IntField(allow_none=True, enums=consts.TODO_STATUS_LIST, default=consts.TODO_STATUS_NEW)
    priority = fields.IntField(allow_none=True, enums=consts.TODO_PRIORITY_LIST, default=consts.TODO_PRIORITY_LOW)
    user_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['user_id'],
            },
        ]
        pass
