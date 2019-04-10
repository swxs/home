# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model

from tornado.web import url
from ..views.Worktable import WorktableHandler

url_mapping = [
    url(r"/api/bi/Worktable/(?:([a-zA-Z0-9&%\.~-]+)/)?", WorktableHandler),
]
