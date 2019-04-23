# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.PasswordLock import PasswordLockHandler

url_mapping = [
    url(r"/api/password_lock/PasswordLock/(?:([a-zA-Z0-9&%\.~-]+)/)?", PasswordLockHandler),
]
