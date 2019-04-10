# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model

from tornado.web import url
from ..views.Artical import ArticalHandler

url_mapping = [
    url(r"/api/multimedia/Artical/(?:([a-zA-Z0-9&%\.~-]+)/)?", ArticalHandler),
]
