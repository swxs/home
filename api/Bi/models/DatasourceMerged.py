# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.DatasourceMerged import *
from .Datasource import Datasource
from mongoengine_utils import NAME_DICT


class DatasourceMerged(Datasource):
    datamerge_id = model.ObjectIdField(helper_text='合表id')

    meta = {
        'indexes': [
            {
                'fields': ['datamerge_id'],
            },
        ],
    }


NAME_DICT["DatasourceMerged"] = DatasourceMerged
