# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model

from tornado.web import url
from ..views.ContainerGroupDatafilter import ContainerGroupDatafilterHandler

url_mapping = [
    url(r"/api/bi/ContainerGroupDatafilter/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerGroupDatafilterHandler),
]
