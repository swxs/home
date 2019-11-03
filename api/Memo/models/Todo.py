# -*- coding: utf-8 -*-
# @File    : Todo.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Todo import *
from ...BaseModel import BaseModelDocument
from settings import instance


@instance.register
class Todo(BaseModelDocument):
    title = fields.StringField(allow_none=True)
    summary = fields.StringField(allow_none=True)
    document = fields.StringField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)
    status = fields.IntField(allow_none=True, enums=TODO_STATUS_LIST, default=TODO_STATUS_NEW)
    priority = fields.IntField(allow_none=True, enums=TODO_PRIORITY_LIST, default=TODO_PRIORITY_LOW)
