# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.ContainerDatafilter import ContainerDatafilterHandler

url_mapping = [
    url(r"/api/bi/ContainerDatafilter/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerDatafilterHandler),
]
