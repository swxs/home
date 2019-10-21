# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Tag import TagHandler

url_mapping = [
    url(r"/api/multimedia/tag/(?:([a-zA-Z0-9&%\.~-]+)/)?", TagHandler),
]