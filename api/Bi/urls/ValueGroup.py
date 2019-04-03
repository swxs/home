# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.ValueGroup import ValueGroupHandler


url_mapping = [
    url(r"/api/ValueGroup/(([a-zA-Z0-9&%\.~-]+)/)?", ValueGroupHandler),
]
