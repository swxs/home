# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model_creater

from ..dao.DatasourceUpload import DatasourceUpload as BaseDatasourceUpload


class DatasourceUpload(BaseDatasourceUpload):
    def __init__(self, **kwargs):
        super(DatasourceUpload, self).__init__(**kwargs)
