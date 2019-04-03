# -*- coding: utf-8 -*-
# @File    : Field.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.Field import FieldHandler


url_mapping = [
    url(r"/api/Field/(([a-zA-Z0-9&%\.~-]+)/)?", FieldHandler),
]
