# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.ContainerDatafilter import ContainerDatafilterHandler


url_mapping = [
    url(r"/api/ContainerDatafilter/(([a-zA-Z0-9&%\.~-]+)/)?", ContainerDatafilterHandler),
]
