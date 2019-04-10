# -*- coding: utf-8 -*-

from tornado.web import url
import api.views.tag as views

url_mapping = [
    url(r"/api/tag/", views.TagHandler),
    url(r"/api/tag/(\w+)/", views.TagHandler),
]
