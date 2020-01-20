# -*- coding: utf-8 -*-
# @File    : Todo.py
# @AUTH    : model_creater

from ..models.Todo import Todo as TodoModel
from ..dao.Todo import Todo as BaseTodo
from marshmallow import Schema, fields

class TodoSchema(TodoModel.Schema):
    pass

class Todo(BaseTodo):
    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)
