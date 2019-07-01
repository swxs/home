# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.DatasourceMerged import *
from .Datasource import Datasource
from document_utils import NAME_DICT


class DatasourceMerged(Datasource):
    datamerge_id = model.ObjectIdField()

    meta = {
        'indexes': [
            {
                'fields': ['datamerge_id'],
            },
        ],
    }


NAME_DICT["DatasourceMerged"] = DatasourceMerged
