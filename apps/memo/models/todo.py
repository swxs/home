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
    title = fields.StringField(
        requirement=False,
    )
    summary = fields.StringField(
        requirement=False,
    )
    document = fields.StringField(
        requirement=False,
    )
    user_id = fields.ObjectIdField(
        requirement=False,
    )
    status = fields.IntField(
        requirement=False,
        enums=consts.TODO_STATUS_LIST,
        default=consts.TODO_STATUS_NEW,
    )
    priority = fields.IntField(
        requirement=False,
        enums=consts.TODO_PRIORITY_LIST,
        default=consts.TODO_PRIORITY_LOW,
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
