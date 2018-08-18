# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @AUTH    : swxs
# @Time    : 2018/8/17 10:04

from tornado.web import url
from api.views import views

import api.urls.user
import api.urls.job
import api.urls.password_lock
import api.urls.artical
import api.urls.todo
import api.urls.tag

__all__ = ["user", "job", "password_lock", "artical", "todo", "tag"]


def get_api_urls():
    url_mapping = [
        url(r"/api/", views.IndexHandler, name='index'),
        url(r"/api/login/", views.LoginHandler, name='login'),
        url(r"/api/logout/", views.LogoutHandler, name='logout'),
    ]
    url_mapping.extend(user.url_mapping)
    url_mapping.extend(tag.url_mapping)
    url_mapping.extend(artical.url_mapping)
    url_mapping.extend(job.url_mapping)
    url_mapping.extend(password_lock.url_mapping)
    url_mapping.extend(todo.url_mapping)
    return url_mapping
