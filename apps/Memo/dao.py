# -*- coding: utf-8 -*-
# @FILE    : dao.py
# @AUTH    : model_creater

import bson
import logging
from dao import fields
from ..BaseDAO import BaseDAO
from . import consts

logger = logging.getLogger("dao")


class Todo(BaseDAO):
    title = fields.StringField()
    summary = fields.StringField()
    document = fields.StringField()
    user_id = fields.ObjectIdField()
    status = fields.IntField(enums=consts.TODO_STATUS_LIST, default=consts.TODO_STATUS_NEW)
    priority = fields.IntField(enums=consts.TODO_PRIORITY_LIST, default=consts.TODO_PRIORITY_LOW)
    user_id = fields.ObjectIdField()

    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)

    @classmethod
    async def get_todo_by_todo_id(cls, todo_id):
        return await cls.find(dict(id=todo_id))
