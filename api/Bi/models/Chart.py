# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine as model
from ..consts.Chart import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Chart(BaseModelDocument):
    name = model.StringField()
    title = model.StringField()
    worktable_id = model.ObjectIdField()
    is_drilldown = model.BooleanField(default=False)
    ttype = model.IntField(enums=CHART_TTYPE_LIST, default=CHART_TTYPE_BAR)
    range_region_type_id = model.ObjectIdField()
    base_option = model.DictField()
    next_chart_id = model.ObjectIdField()
    prev_chart_id = model.ObjectIdField()
    custom_attr = model.DictField()
    markline = model.ListField()


NAME_DICT["Chart"] = Chart
