# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.ContainerGroup import ContainerGroupHandler

url_mapping = [
    url(r"/api/bi/ContainerGroup/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerGroupHandler),
]
