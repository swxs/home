# -*- coding: utf-8 -*-

from tornado.web import url
import views as views

url_mapping = [
    url(r"/api/user/(\w+)/", views.UserHandler, name='api_select_user'),
    url(r"/api/user/", views.UserHandler, name='api_select_users'),
    url(r"/api/user/", views.UserHandler, name='api_create_user'),
    url(r"/api/user/(\w+)/", views.UserHandler, name='api_update_user'),
    url(r"/api/user/(\w+)/", views.UserHandler, name='api_modify_user'),
    url(r"/api/user/(\w+)/", views.UserHandler, name='api_delete_user'),
]
