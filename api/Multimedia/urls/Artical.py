# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.Artical import ArticalHandler


url_mapping = [
    url(r"/api/Artical/(([a-zA-Z0-9&%\.~-]+)/)?", ArticalHandler),
]
