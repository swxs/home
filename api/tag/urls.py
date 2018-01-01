# -*- coding: utf-8 -*-

from tornado.web import url
import views as views

url_mapping = [
    url(r"/api/tag/(\w+)/", views.TagHandler, name='api_select_tag'),
    url(r"/api/tag/", views.TagHandler, name='api_select_tags'),
    url(r"/api/tag/", views.TagHandler, name='api_create_tag'),
    url(r"/api/tag/(\w+)/", views.TagHandler, name='api_update_tag'),
    url(r"/api/tag/(\w+)/", views.TagHandler, name='api_modify_tag'),
    url(r"/api/tag/(\w+)/", views.TagHandler, name='api_delete_tag'),
]
