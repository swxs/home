# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine as model
from ..consts.DatasourceMerged import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class DatasourceMerged(BaseModelDocument):
    datamerge_id = model.ObjectIdField(helper_text='合表id')

    meta = {
        'indexes': [
            {
                'fields': ['datamerge_id'],
            },
        ]
    }

NAME_DICT["DatasourceMerged"] = DatasourceMerged
