# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.DatasourceRegion import *
from .Datasource import Datasource
from document_utils import NAME_DICT


class DatasourceRegion(Datasource):
    region_type_id = model.ObjectIdField()

    meta = {
        'indexes': [
            {
                'fields': ['region_type_id'],
            },
        ],
    }


NAME_DICT["DatasourceRegion"] = DatasourceRegion
