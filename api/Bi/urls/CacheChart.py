# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.CacheChart import CacheChartHandler

url_mapping = [
    url(r"/api/bi/CacheChart/(?:([a-zA-Z0-9&%\.~-]+)/)?", CacheChartHandler),
]
