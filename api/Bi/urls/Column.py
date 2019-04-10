# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model

from tornado.web import url
from ..views.Column import ColumnHandler

url_mapping = [
    url(r"/api/bi/Column/(?:([a-zA-Z0-9&%\.~-]+)/)?", ColumnHandler),
]
