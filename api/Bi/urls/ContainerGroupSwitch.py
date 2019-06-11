# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.ContainerGroupSwitch import ContainerGroupSwitchHandler

url_mapping = [
    url(r"/api/bi/container_group_switch/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerGroupSwitchHandler),
]
