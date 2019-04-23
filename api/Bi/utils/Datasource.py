# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model_creater

from ..commons.Datasource import Datasource as BaseDatasource


class Datasource(BaseDatasource):
    def __init__(self, **kwargs):
        super(Datasource, self).__init__(**kwargs)
