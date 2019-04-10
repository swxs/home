# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @AUTH    : swxs
# @Time    : 2018/4/30 14:52

from api.models.user import User
from api.models.artical import Artical
from api.models.job import Job
from api.models.password_lock import PasswordLock
from api.models.tag import Tag
from api.models.todo import Todo
from api.models.movie import Movie
from api.bi.models.CacheChart import Cachechart

__all__ = [
    "User",
    "Artical",
    "Job",
    "Tag",
    "PasswordLock",
    "Todo",
    "Movie",
    "Cachechart",
]
