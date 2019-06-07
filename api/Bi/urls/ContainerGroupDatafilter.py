# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.ContainerGroupDatafilter import ContainerGroupDatafilterHandler

url_mapping = [
    url(r"/api/bi/container_group_datafilter/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerGroupDatafilterHandler),
]
