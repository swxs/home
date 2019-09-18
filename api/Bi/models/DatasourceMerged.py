# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.DatasourceMerged import *
from .Datasource import Datasource
from settings import instance
from document_utils import NAME_DICT

@instance.register
class DatasourceMerged(Datasource):
    datamerge_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['datamerge_id'],
            },
        ]
        pass


NAME_DICT["DatasourceMerged"] = DatasourceMerged
