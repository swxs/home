# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Dashboard import DashboardHandler

url_mapping = [
    url(r"/api/bi/dashboard/(?:([a-zA-Z0-9&%\.~-]+)/)?", DashboardHandler),
]
