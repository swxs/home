# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model_creater

from ..dao.Datafilter import Datafilter as BaseDatafilter


class Datafilter(BaseDatafilter):
    def __init__(self, **kwargs):
        super(Datafilter, self).__init__(**kwargs)
