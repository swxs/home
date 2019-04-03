# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.Column import ColumnHandler


url_mapping = [
    url(r"/api/Column/(([a-zA-Z0-9&%\.~-]+)/)?", ColumnHandler),
]
