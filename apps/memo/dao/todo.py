# -*- coding: utf-8 -*-
# @File    : dao/todo.py
# @AUTH    : code_creater

import logging
import datetime

import bson

from dao import BaseDocument, fields

# 本模块方法
from .. import consts
from ..models.todo import Todo as TodoModel

logger = logging.getLogger("main.apps.memo.dao.todo")


class Todo(BaseDocument):
    title = fields.StringField(allow_none=True)
    summary = fields.StringField(allow_none=True)
    document = fields.StringField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)
    status = fields.IntField(allow_none=True, enums=consts.TODO_STATUS_LIST, default=consts.TODO_STATUS_NEW)
    priority = fields.IntField(allow_none=True, enums=consts.TODO_PRIORITY_LIST, default=consts.TODO_PRIORITY_LOW)
    user_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        model = TodoModel
        manager = "umongo_motor"
        memorizer = "none"

    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)
