# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model

from tornado.web import url
from ..views.Publish import PublishHandler

url_mapping = [
    url(r"/api/bi/Publish/(?:([a-zA-Z0-9&%\.~-]+)/)?", PublishHandler),
]
