# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Datasource import DatasourceHandler

url_mapping = [
    url(r"/api/bi/Datasource/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatasourceHandler),
]
