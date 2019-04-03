# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.DatasourceRegion import DatasourceRegionHandler


url_mapping = [
    url(r"/api/DatasourceRegion/(([a-zA-Z0-9&%\.~-]+)/)?", DatasourceRegionHandler),
]
