# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model_creater

from ..dao.Worktable import Worktable as BaseWorktable


class Worktable(BaseWorktable):
    def __init__(self, **kwargs):
        super(Worktable, self).__init__(**kwargs)
