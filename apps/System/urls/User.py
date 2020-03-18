# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.User import UserHandler

url_mapping = [
    url(r"/api/system/user/(?:([a-zA-Z0-9&%\.~-]+)/)?", UserHandler),
]
