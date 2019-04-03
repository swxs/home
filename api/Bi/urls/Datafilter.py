# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.Datafilter import DatafilterHandler


url_mapping = [
    url(r"/api/Datafilter/(([a-zA-Z0-9&%\.~-]+)/)?", DatafilterHandler),
]
