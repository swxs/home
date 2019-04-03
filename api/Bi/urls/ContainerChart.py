# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.ContainerChart import ContainerChartHandler


url_mapping = [
    url(r"/api/ContainerChart/(([a-zA-Z0-9&%\.~-]+)/)?", ContainerChartHandler),
]
