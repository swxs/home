# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.ContainerGroup import ContainerGroupHandler


url_mapping = [
    url(r"/api/ContainerGroup/(([a-zA-Z0-9&%\.~-]+)/)?", ContainerGroupHandler),
]
