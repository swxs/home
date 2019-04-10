# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model

from tornado.web import url
from ..views.ValueGroup import ValueGroupHandler

url_mapping = [
    url(r"/api/bi/ValueGroup/(?:([a-zA-Z0-9&%\.~-]+)/)?", ValueGroupHandler),
]
