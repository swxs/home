# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.Datamerge import DatamergeHandler


url_mapping = [
    url(r"/api/Datamerge/(([a-zA-Z0-9&%\.~-]+)/)?", DatamergeHandler),
]
