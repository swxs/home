# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model

from tornado.web import url
from ..views.ContainerChart import ContainerChartHandler

url_mapping = [
    url(r"/api/bi/ContainerChart/(?:([a-zA-Z0-9&%\.~-]+)/)?", ContainerChartHandler),
]
