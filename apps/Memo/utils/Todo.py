# -*- coding: utf-8 -*-
# @File    : Todo.py
# @AUTH    : model_creater

from ..dao.Todo import Todo as BaseTodo


class Todo(BaseTodo):
    def __init__(self, **kwargs):
        super(Todo, self).__init__(**kwargs)
