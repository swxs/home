# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.PasswordLock import PasswordLockHandler


url_mapping = [
    url(r"/api/PasswordLock/(([a-zA-Z0-9&%\.~-]+)/)?", PasswordLockHandler),
]
