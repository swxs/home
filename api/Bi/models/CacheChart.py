# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.CacheChart import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class CacheChart(BaseModelDocument):
    chart_id = model.ObjectIdField()
    data_filter_id = model.ObjectIdField()
    ttype = model.IntField(enums=CACHE_CHART_TTYPE_LIST)
    key = model.StringField()
    value = model.StringField()
    status = model.IntField(enums=CACHE_CHART_STATUS_LIST)


NAME_DICT["CacheChart"] = CacheChart
