# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model_creater

from tornado.web import url
from ..views.Worktable import WorktableHandler

url_mapping = [
    url(r"/api/bi/worktable/(?:([a-zA-Z0-9&%\.~-]+)/)?", WorktableHandler),
]
