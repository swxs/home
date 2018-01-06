# -*- coding: utf-8 -*-

from tornado.web import url
import views as views
from api.tag import views as tag_views

url_mapping = [
    url(r"/api/", views.IndexHandler, name='index'),
    url(r"/api/tag/(\w+)/", tag_views.TagHandler, name='api_select_tag'),
    url(r"/api/tag/", tag_views.TagHandler, name='api_select_tags'),
    url(r"/api/tag/", tag_views.TagHandler, name='api_create_tag'),
    url(r"/api/tag/(\w+)/", tag_views.TagHandler, name='api_update_tag'),
    url(r"/api/tag/(\w+)/", tag_views.TagHandler, name='api_modify_tag'),
    url(r"/api/tag/(\w+)/", tag_views.TagHandler, name='api_delete_tag'),
]

# url_mapping.append(tag_urls)