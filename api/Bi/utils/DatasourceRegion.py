# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model_creater

from ..commons.DatasourceRegion import DatasourceRegion as BaseDatasourceRegion


class DatasourceRegion(BaseDatasourceRegion):
    def __init__(self, **kwargs):
        super(DatasourceRegion, self).__init__(**kwargs)
