# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model

from tornado.web import url
from ..views.ContainerGroupSwitch import ContainerGroupSwitchHandler

url_mapping = [
    url(r"/api/bi/ContainerGroupSwitch/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerGroupSwitchHandler),
]
