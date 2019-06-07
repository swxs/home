# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.DatasourceUpload import DatasourceUploadHandler

url_mapping = [
    url(r"/api/bi/datasource_upload/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatasourceUploadHandler),
]
