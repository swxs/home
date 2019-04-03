# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.Container import ContainerHandler


url_mapping = [
    url(r"/api/Container/(([a-zA-Z0-9&%\.~-]+)/)?", ContainerHandler),
]
