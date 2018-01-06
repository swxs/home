# -*- coding: utf-8 -*-

from tornado.web import url
import views as views

url_mapping = [
    url(r"/api/artical/(\w+)/", views.ArticalHandler, name='api_select_artical'),
    url(r"/api/artical/", views.ArticalHandler, name='api_select_articals'),
    url(r"/api/artical/", views.ArticalHandler, name='api_create_artical'),
    url(r"/api/artical/(\w+)/", views.ArticalHandler, name='api_update_artical'),
    url(r"/api/artical/(\w+)/", views.ArticalHandler, name='api_modify_artical'),
    url(r"/api/artical/(\w+)/", views.ArticalHandler, name='api_delete_artical'),
]
