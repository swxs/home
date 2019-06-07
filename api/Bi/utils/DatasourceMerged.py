# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model_creater

from ..dao.DatasourceMerged import DatasourceMerged as BaseDatasourceMerged


class DatasourceMerged(BaseDatasourceMerged):
    def __init__(self, **kwargs):
        super(DatasourceMerged, self).__init__(**kwargs)
