# -*- coding: utf-8 -*-
# @File    : dao/todo.py
# @AUTH    : code_creater

import logging
import datetime

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.todo import Todo as TodoModel

logger = logging.getLogger("main.apps.memo.dao.todo")


class Todo(BaseDocument):
    id = fields.PrimaryField()
    created = fields.DateTimeField(
        default_create=datetime.datetime.now,
    )
    updated = fields.DateTimeField(
        default_create=datetime.datetime.now,
        default_update=datetime.datetime.now,
    )
    user_id = fields.ObjectIdField()
    title = fields.StringField()
    summary = fields.StringField()
    document = fields.StringField()
    status = fields.IntField(
        enums=consts.TODO_STATUS_LIST,
        default_create=consts.TODO_STATUS_NEW,
    )
    priority = fields.IntField(
        enums=consts.TODO_PRIORITY_LIST,
        default_create=consts.TODO_PRIORITY_LOW,
    )

    class Meta:
        model = TodoModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)
