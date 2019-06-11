# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model_creater

from ..dao.Datasource import Datasource as BaseDatasource


class Datasource(BaseDatasource):
    def __init__(self, **kwargs):
        super(Datasource, self).__init__(**kwargs)
