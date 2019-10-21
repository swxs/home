# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.DatasourceRegion import DatasourceRegionHandler

url_mapping = [
    url(r"/api/bi/datasource_region/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatasourceRegionHandler),
]