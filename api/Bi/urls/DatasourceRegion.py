# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model

from tornado.web import url
from ..views.DatasourceRegion import DatasourceRegionHandler

url_mapping = [
    url(r"/api/bi/DatasourceRegion/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatasourceRegionHandler),
]
