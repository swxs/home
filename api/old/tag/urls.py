# -*- coding: utf-8 -*-

from tornado.web import url
import api.tag.views as views

url_mapping = [
    url(r"/api/tag/(\w+)/", views.TagHandler, name='select_tag'),
    url(r"/api/tag/", views.TagHandler, name='select_tag_list'),
    url(r"/api/tag/", views.TagHandler, name='create_tag'),
    url(r"/api/tag/(\w+)/", views.TagHandler, name='update_tag'),
    url(r"/api/tag/(\w+)/", views.TagHandler, name='modify_tag'),
    url(r"/api/tag/(\w+)/", views.TagHandler, name='delete_tag'),
]
