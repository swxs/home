# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model_creater

from ..commons.Artical import Artical as BaseArtical


class Artical(BaseArtical):
    def __init__(self, **kwargs):
        super(Artical, self).__init__(**kwargs)
