# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.DatasourceMerged import DatasourceMergedHandler


url_mapping = [
    url(r"/api/DatasourceMerged/(([a-zA-Z0-9&%\.~-]+)/)?", DatasourceMergedHandler),
]
