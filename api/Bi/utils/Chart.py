# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model_creater

from ..dao.Chart import Chart as BaseChart


class Chart(BaseChart):
    def __init__(self, **kwargs):
        super(Chart, self).__init__(**kwargs)
