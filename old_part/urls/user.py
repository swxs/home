# -*- coding: utf-8 -*-
# @File    : urls.py
# @AUTH    : swxs
# @Time    : 2018/5/5 11:40


from tornado.web import url
import api.views.user as views

url_mapping = [
    url(r"/api/user/", views.UserHandler),
    url(r"/api/user/(\w+)/", views.UserHandler),
]
