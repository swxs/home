# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.ContainerGroupSwitch import ContainerGroupSwitchHandler


url_mapping = [
    url(r"/api/ContainerGroupSwitch/(([a-zA-Z0-9&%\.~-]+)/)?", ContainerGroupSwitchHandler),
]
