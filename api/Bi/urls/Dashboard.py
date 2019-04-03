# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.Dashboard import DashboardHandler


url_mapping = [
    url(r"/api/Dashboard/(([a-zA-Z0-9&%\.~-]+)/)?", DashboardHandler),
]
