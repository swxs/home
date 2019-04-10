# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model

from tornado.web import url
from ..views.Dashboard import DashboardHandler

url_mapping = [
    url(r"/api/bi/Dashboard/(?:([a-zA-Z0-9&%\.~-]+)/)?", DashboardHandler),
]
