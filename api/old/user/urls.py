# -*- coding: utf-8 -*-

from tornado.web import url
import api.user.views as views

url_mapping = [
    url(r"/api/user/(\w+)/", views.UserHandler, name='select_user'),
    url(r"/api/user/", views.UserHandler, name='select_user_list'),
    url(r"/api/user/", views.UserHandler, name='create_user'),
    url(r"/api/user/(\w+)/", views.UserHandler, name='update_user'),
    url(r"/api/user/(\w+)/", views.UserHandler, name='modify_user'),
    url(r"/api/user/(\w+)/", views.UserHandler, name='delete_user'),
]
