# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.DatasourceMerged import DatasourceMergedHandler

url_mapping = [
    url(r"/api/bi/datasource_merged/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatasourceMergedHandler),
]
