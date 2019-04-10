# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model

from tornado.web import url
from ..views.Container import ContainerHandler

url_mapping = [
    url(r"/api/bi/Container/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerHandler),
]
