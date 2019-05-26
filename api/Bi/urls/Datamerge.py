# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Datamerge import DatamergeHandler

url_mapping = [
    url(r"/api/bi/Datamerge/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatamergeHandler),
]
