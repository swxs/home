# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.Publish import PublishHandler


url_mapping = [
    url(r"/api/Publish/(([a-zA-Z0-9&%\.~-]+)/)?", PublishHandler),
]
