# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model

from tornado.web import url
from ..views.Ttype import TtypeHandler

url_mapping = [
    url(r"/api/multimedia/Ttype/(?:([a-zA-Z0-9&%\.~-]+)/)?", TtypeHandler),
]
