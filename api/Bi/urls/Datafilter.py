# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Datafilter import DatafilterHandler

url_mapping = [
    url(r"/api/bi/datafilter/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatafilterHandler),
]
