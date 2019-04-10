# -*- coding: utf-8 -*-

from tornado.web import url
import api.views.todo as views

url_mapping = [
    url(r"/api/todo/", views.TodoHandler),
    url(r"/api/todo/(\w+)/", views.TodoHandler),
]
