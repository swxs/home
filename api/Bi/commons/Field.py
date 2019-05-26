# -*- coding: utf-8 -*-
# @File    : Field.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Field import Field as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Field(BaseUtils):
    chart_id = model.ObjectIdField()
    name = model.StringField()
    display_name = model.StringField()
    column_id = model.ObjectIdField()
    is_unique = model.BooleanField()
    agg_type = model.IntField()
    multi_agg_type = model.IntField()
    sort_type = model.BooleanField()
    date_type = model.IntField()
    sort_region_type_id = model.ObjectIdField()
    ttype = model.IntField()
    dtype = model.IntField()
    stype = model.IntField()
    range_region_type_id = model.ObjectIdField()
    custom_attr = model.DictField()

    def __init__(self, **kwargs):
        super(Field, self).__init__(**kwargs)

    @property
    def chart(self):
        from .Chart import Chart
        return Chart.get_chart_by_chart_id(self.chart_id)

    @property
    def column(self):
        from .Column import Column
        return Column.get_column_by_column_id(self.column_id)

    @classmethod
    def get_field_by_field_id(cls, field_id):
        return cls.select(id=field_id)

