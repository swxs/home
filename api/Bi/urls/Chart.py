# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.Chart import ChartHandler


url_mapping = [
    url(r"/api/Chart/(([a-zA-Z0-9&%\.~-]+)/)?", ChartHandler),
]
