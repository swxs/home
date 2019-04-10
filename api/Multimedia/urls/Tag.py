# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model

from tornado.web import url
from ..views.Tag import TagHandler

url_mapping = [
    url(r"/api/multimedia/Tag/(?:([a-zA-Z0-9&%\.~-]+)/)?", TagHandler),
]
