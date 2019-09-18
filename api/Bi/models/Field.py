# -*- coding: utf-8 -*-
# @File    : Field.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Field import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Field(BaseModelDocument):
    chart_id = fields.ObjectIdField(allow_none=True)
    name = fields.StringField(allow_none=True)
    display_name = fields.StringField(allow_none=True)
    column_id = fields.ObjectIdField(allow_none=True)
    is_unique = fields.BooleanField(allow_none=True, default=False)
    agg_type = fields.IntField(allow_none=True, enums=FIELD_AGG_TYPE_LIST)
    multi_agg_type = fields.IntField(allow_none=True, enums=FIELD_MULTI_AGG_TYPE_LIST)
    sort_type = fields.BooleanField(allow_none=True)
    date_type = fields.IntField(allow_none=True, enums=FIELD_DATE_TYPE_LIST)
    sort_region_type_id = fields.ObjectIdField(allow_none=True)
    ttype = fields.IntField(allow_none=True, enums=FIELD_TTYPE_LIST)
    dtype = fields.IntField(allow_none=True, enums=FIELD_DTYPE_LIST)
    stype = fields.IntField(allow_none=True, enums=FIELD_STYPE_LIST)
    range_region_type_id = fields.ObjectIdField(allow_none=True)
    custom_attr = fields.DictField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['chart_id'],
            },
            {
                'key': ['chart_id', 'stype'],
            },
        ]
        pass


NAME_DICT["Field"] = Field
