# -*- coding: utf-8 -*-

from tornado.web import url
import api.views.password_lock as views

url_mapping = [
    url(r"/api/password_lock/", views.PasswordLockHandler),
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler),
]
