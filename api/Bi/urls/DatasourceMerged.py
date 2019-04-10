# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model

from tornado.web import url
from ..views.DatasourceMerged import DatasourceMergedHandler

url_mapping = [
    url(r"/api/bi/DatasourceMerged/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatasourceMergedHandler),
]
