# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from tornado.web import url
from ..views.Worktable import WorktableHandler


url_mapping = [
    url(r"/api/Worktable/(([a-zA-Z0-9&%\.~-]+)/)?", WorktableHandler),
]
