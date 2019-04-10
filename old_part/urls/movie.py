# -*- coding: utf-8 -*-

from tornado.web import url
import api.views.movie as views

url_mapping = [
    url(r"/api/movie/", views.MovieHandler),
    url(r"/api/movie/(\w+)/", views.MovieHandler),
]
