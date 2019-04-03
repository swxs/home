# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from tornado.web import url
from ..views.Ttype import TtypeHandler


url_mapping = [
    url(r"/api/Ttype/(([a-zA-Z0-9&%\.~-]+)/)?", TtypeHandler),
]
