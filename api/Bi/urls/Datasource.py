# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.Datasource import DatasourceHandler


url_mapping = [
    url(r"/api/Datasource/(([a-zA-Z0-9&%\.~-]+)/)?", DatasourceHandler),
]
