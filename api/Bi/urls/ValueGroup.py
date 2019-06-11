# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.ValueGroup import ValueGroupHandler

url_mapping = [
    url(r"/api/bi/value_group/(?:([a-zA-Z0-9&%\.~-]+)/)?", ValueGroupHandler),
]
