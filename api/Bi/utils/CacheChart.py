# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model_creater

from ..commons.CacheChart import CacheChart as BaseCacheChart


class CacheChart(BaseCacheChart):
    def __init__(self, **kwargs):
        super(CacheChart, self).__init__(**kwargs)
