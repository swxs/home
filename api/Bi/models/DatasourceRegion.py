# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.DatasourceRegion import *
from .Datasource import Datasource
from settings import instance
from document_utils import NAME_DICT

@instance.register
class DatasourceRegion(Datasource):
    region_type_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['region_type_id'],
            },
        ]
        pass


NAME_DICT["DatasourceRegion"] = DatasourceRegion
