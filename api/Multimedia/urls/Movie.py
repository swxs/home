# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.Movie import MovieHandler


url_mapping = [
    url(r"/api/Movie/(([a-zA-Z0-9&%\.~-]+)/)?", MovieHandler),
]
