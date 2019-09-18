# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.CacheChart import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class CacheChart(BaseModelDocument):
    chart_id = fields.ObjectIdField(allow_none=True)
    data_filter_id = fields.ObjectIdField(allow_none=True)
    ttype = fields.IntField(allow_none=True, enums=CACHE_CHART_TTYPE_LIST)
    key = fields.StringField(allow_none=True)
    value = fields.StringField(allow_none=True)
    status = fields.IntField(allow_none=True, enums=CACHE_CHART_STATUS_LIST)


NAME_DICT["CacheChart"] = CacheChart
