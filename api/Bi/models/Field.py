# -*- coding: utf-8 -*-
# @File    : Field.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Field import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Field(BaseModelDocument):
    chart_id = model.ObjectIdField()
    name = model.StringField()
    display_name = model.StringField()
    column_id = model.ObjectIdField()
    is_unique = model.BooleanField(default=False)
    agg_type = model.IntField(enums=FIELD_AGG_TYPE_LIST)
    multi_agg_type = model.IntField(enums=FIELD_MULTI_AGG_TYPE_LIST)
    sort_type = model.BooleanField()
    date_type = model.IntField(enums=FIELD_DATE_TYPE_LIST)
    sort_region_type_id = model.ObjectIdField()
    ttype = model.IntField(enums=FIELD_TTYPE_LIST)
    dtype = model.IntField(enums=FIELD_DTYPE_LIST)
    stype = model.IntField(enums=FIELD_STYPE_LIST)
    range_region_type_id = model.ObjectIdField()
    custom_attr = model.DictField()

    meta = {
        'indexes': [
            {
                'fields': ['chart_id'],
            },
            {
                'fields': ['chart_id', 'stype'],
            },
        ],
    }


NAME_DICT["Field"] = Field
