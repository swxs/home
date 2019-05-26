# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model_creater

from ..commons.Datamerge import Datamerge as BaseDatamerge


class Datamerge(BaseDatamerge):
    def __init__(self, **kwargs):
        super(Datamerge, self).__init__(**kwargs)
