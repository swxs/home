# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model_creater

from ..dao.Ttype import Ttype as BaseTtype


class Ttype(BaseTtype):
    def __init__(self, **kwargs):
        super(Ttype, self).__init__(**kwargs)
