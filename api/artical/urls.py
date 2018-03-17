# -*- coding: utf-8 -*-

from tornado.web import url
import api.artical.views as views

url_mapping = [
    url(r"/api/artical/(\w+)/", views.ArticalHandler, name='select_artical'),
    url(r"/api/artical/", views.ArticalHandler, name='select_artical_list'),
    url(r"/api/artical/", views.ArticalHandler, name='create_artical'),
    url(r"/api/artical/(\w+)/", views.ArticalHandler, name='update_artical'),
    url(r"/api/artical/(\w+)/", views.ArticalHandler, name='modify_artical'),
    url(r"/api/artical/(\w+)/", views.ArticalHandler, name='delete_artical'),
]
