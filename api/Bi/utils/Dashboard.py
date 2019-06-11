# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model_creater

from ..dao.Dashboard import Dashboard as BaseDashboard


class Dashboard(BaseDashboard):
    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)
