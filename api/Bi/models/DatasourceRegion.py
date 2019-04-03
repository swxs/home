# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine as model
from ..consts.DatasourceRegion import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class DatasourceRegion(BaseModelDocument):
    region_type_id = model.ObjectIdField(helper_text='层级id')

    meta = {
        'indexes': [
            {
                'fields': ['region_type_id'],
            },
        ]
    }

NAME_DICT["DatasourceRegion"] = DatasourceRegion
