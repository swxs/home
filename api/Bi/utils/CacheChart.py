# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.CacheChart import CacheChart as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class CacheChart(BaseUtils):
    chart_id = model.ObjectIdField()
    data_filter_id = model.ObjectIdField()
    ttype = model.IntField()
    key = model.StringField()
    value = model.StringField()
    status = model.IntField()

    def __init__(self, **kwargs):
        super(CacheChart, self).__init__(**kwargs)

