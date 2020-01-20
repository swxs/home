# -*- coding: utf-8 -*-
# @File    : Todo.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from document_utils.consts import NAME_DICT
from ..models.Todo import Todo as TodoModel
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/todo")


class Todo(BaseDAO):
    title = model.StringField()
    summary = model.StringField()
    document = model.StringField()
    user_id = model.ObjectIdField()
    status = model.IntField()
    priority = model.IntField()

    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)

    @classmethod
    async def get_todo_by_todo_id(cls, todo_id):
        return await cls.select(id=todo_id)


NAME_DICT[BaseDAO.__manager__]["Todo"] = TodoModel