# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.DatasourceUpload import DatasourceUploadHandler


url_mapping = [
    url(r"/api/DatasourceUpload/(([a-zA-Z0-9&%\.~-]+)/)?", DatasourceUploadHandler),
]
