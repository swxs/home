# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.Tag import TagHandler


url_mapping = [
    url(r"/api/Tag/(([a-zA-Z0-9&%\.~-]+)/)?", TagHandler),
]
