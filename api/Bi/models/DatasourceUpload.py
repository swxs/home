# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.DatasourceUpload import *
from .Datasource import Datasource
from settings import instance
from document_utils import NAME_DICT

@instance.register
class DatasourceUpload(Datasource):
    filename = fields.StringField(allow_none=True)

    class Meta:
        pass


NAME_DICT["DatasourceUpload"] = DatasourceUpload
