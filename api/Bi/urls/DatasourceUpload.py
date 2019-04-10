# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model

from tornado.web import url
from ..views.DatasourceUpload import DatasourceUploadHandler

url_mapping = [
    url(r"/api/bi/DatasourceUpload/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatasourceUploadHandler),
]
