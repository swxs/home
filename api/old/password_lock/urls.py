# -*- coding: utf-8 -*-

from tornado.web import url
import api.password_lock.views as views

url_mapping = [
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler, name='select_password_lock'),
    url(r"/api/password_lock/", views.PasswordLockHandler, name='select_password_lock_list'),
    url(r"/api/password_lock/", views.PasswordLockHandler, name='create_password_lock'),
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler, name='update_password_lock'),
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler, name='modify_password_lock'),
    url(r"/api/password_lock/(\w+)/", views.PasswordLockHandler, name='delete_password_lock'),
]
