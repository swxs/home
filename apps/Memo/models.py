# -*- coding: utf-8 -*-
# @FILE    : models.py
# @AUTH    : model_creater

import bson
import datetime
from umongo import Instance, Document, fields
from dao.manager.manager_umongo_motor import NAME_DICT
from ..BaseModel import BaseModelDocument
from . import consts
from settings import instance


@instance.register
class Todo(BaseModelDocument):
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


NAME_DICT["Todo"] = Todo
