# -*- coding: utf-8 -*-
# @File    : Todo.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Todo import TodoHandler

url_mapping = [
    url(r"/api/memo/todo/(?:([a-zA-Z0-9&%\.~-]+)/)?", TodoHandler),
]
