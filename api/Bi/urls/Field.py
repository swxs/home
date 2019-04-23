# -*- coding: utf-8 -*-
# @File    : Field.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Field import FieldHandler

url_mapping = [
    url(r"/api/bi/Field/(?:([a-zA-Z0-9&%\.~-]+)/)?", FieldHandler),
]
