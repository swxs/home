# -*- coding: utf-8 -*-

from tornado.web import url
import views as views

url_mapping = [
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler, name='api_select_password_lock'),
    url(r"/api/password_lock/", views.PasswordLockHandler, name='api_select_password_locks'),
    url(r"/api/password_lock/", views.PasswordLockHandler, name='api_create_password_lock'),
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler, name='api_update_password_lock'),
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler, name='api_modify_password_lock'),
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler, name='api_delete_password_lock'),
]
