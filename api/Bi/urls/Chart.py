# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model

from tornado.web import url
from ..views.Chart import ChartHandler

url_mapping = [
    url(r"/api/bi/Chart/(?:([a-zA-Z0-9&%\.~-]+)/)?", ChartHandler),
]
