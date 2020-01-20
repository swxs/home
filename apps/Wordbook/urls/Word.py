# -*- coding: utf-8 -*-
# @File    : Word.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Word import WordHandler

url_mapping = [
    url(r"/api/wordbook/word/(?:([a-zA-Z0-9&%\.~-]+)/)?", WordHandler),
]
