# -*- coding: utf-8 -*-
# @File    : Todo.py
# @AUTH    : model_creater

from ..models import Todo as TodoModel
from ..dao import Todo as BaseTodo
from marshmallow import Schema, fields

TodoSchema = TodoModel.schema.as_marshmallow_schema()

todo_schema = TodoSchema()


class Todo(BaseTodo):
    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)
