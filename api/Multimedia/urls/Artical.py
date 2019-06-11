# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Artical import ArticalHandler

url_mapping = [
    url(r"/api/multimedia/artical/(?:([a-zA-Z0-9&%\.~-]+)/)?", ArticalHandler),
]
