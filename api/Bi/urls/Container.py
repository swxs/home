# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Container import ContainerHandler

url_mapping = [
    url(r"/api/bi/container/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerHandler),
]
