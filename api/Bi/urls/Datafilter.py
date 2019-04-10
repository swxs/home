# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model

from tornado.web import url
from ..views.Datafilter import DatafilterHandler

url_mapping = [
    url(r"/api/bi/Datafilter/(?:([a-zA-Z0-9&%\.~-]+)/)?", DatafilterHandler),
]
