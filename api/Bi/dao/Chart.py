# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Chart import Chart as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Chart(BaseDAO):
    name = model.StringField()
    title = model.StringField()
    worktable_id = model.ObjectIdField()
    is_drilldown = model.BooleanField()
    ttype = model.IntField()
    range_region_type_id = model.ObjectIdField()
    base_option = model.DictField()
    next_chart_id = model.ObjectIdField()
    prev_chart_id = model.ObjectIdField()
    custom_attr = model.DictField()
    markline = model.ListField()

    def __init__(self, **kwargs):
        super(Chart, self).__init__(**kwargs)

    @property
    def worktable(self):
        from .Worktable import Worktable
        return Worktable.get_worktable_by_worktable_id(self.worktable_id)

    @classmethod
    def get_chart_by_chart_id(cls, chart_id):
        return cls.select(id=chart_id)
