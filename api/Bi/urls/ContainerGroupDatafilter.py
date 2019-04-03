# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.ContainerGroupDatafilter import ContainerGroupDatafilterHandler


url_mapping = [
    url(r"/api/ContainerGroupDatafilter/(([a-zA-Z0-9&%\.~-]+)/)?", ContainerGroupDatafilterHandler),
]
