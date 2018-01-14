# -*- coding: utf-8 -*-

from tornado.web import url
import api.user_views.user_password_lock as user_password_lock_views

url_mapping = [
    url(r"/api/user/password_lock/(\w+)/", user_password_lock_views.UserPasswordLockHandler, name='api_select_password_lock'),
    url(r"/api/user/password_lock/", user_password_lock_views.UserPasswordLockHandler, name='api_select_password_locks'),
    url(r"/api/user/password_lock/", user_password_lock_views.UserPasswordLockHandler, name='api_create_password_lock'),
    url(r"/api/user/password_lock/(\w+)/", user_password_lock_views.UserPasswordLockHandler, name='api_update_password_lock'),
    url(r"/api/user/password_lock/(\w+)/", user_password_lock_views.UserPasswordLockHandler, name='api_modify_password_lock'),
    url(r"/api/user/password_lock/(\w+)/", user_password_lock_views.UserPasswordLockHandler, name='api_delete_password_lock'),
]
