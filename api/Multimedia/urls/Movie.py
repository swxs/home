# -*- coding: utf-8 -*-
# @File    : Movie.py
# @AUTH    : model

from tornado.web import url
from ..views.Movie import MovieHandler

url_mapping = [
    url(r"/api/multimedia/Movie/(?:([a-zA-Z0-9&%\.~-]+)/)?", MovieHandler),
]
