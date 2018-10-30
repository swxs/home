# -*- coding: utf-8 -*-

from tornado.web import url
import api.views.artical as views

url_mapping = [
    url(r"/api/artical/", views.ArticalHandler),
    url(r"/api/artical/(\w+)/", views.ArticalHandler),

]
