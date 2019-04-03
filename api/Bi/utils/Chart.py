# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine_utils as model
from ..models.Chart import Chart as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Chart(BaseUtils):
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
