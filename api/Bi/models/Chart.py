# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Chart import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Chart(BaseModelDocument):
    name = fields.StringField(allow_none=True)
    title = fields.StringField(allow_none=True)
    worktable_id = fields.ObjectIdField(allow_none=True)
    is_drilldown = fields.BooleanField(allow_none=True, default=False)
    ttype = fields.IntField(allow_none=True, enums=CHART_TTYPE_LIST, default=CHART_TTYPE_BAR)
    range_region_type_id = fields.ObjectIdField(allow_none=True)
    base_option = fields.DictField(allow_none=True)
    next_chart_id = fields.ObjectIdField(allow_none=True)
    prev_chart_id = fields.ObjectIdField(allow_none=True)
    custom_attr = fields.DictField(allow_none=True)
    markline = fields.ListField(fields.StringField(), allow_none=True)


NAME_DICT["Chart"] = Chart
