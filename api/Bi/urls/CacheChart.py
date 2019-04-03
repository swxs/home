# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.CacheChart import CacheChartHandler


url_mapping = [
    url(r"/api/CacheChart/(([a-zA-Z0-9&%\.~-]+)/)?", CacheChartHandler),
]
