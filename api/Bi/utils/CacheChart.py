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

    @property
    def chart(self):
        from .Chart import Chart
        return Chart.get_chart_by_chart_id(self.chart_id)

    @property
    def datafilter(self):
        from .Datafilter import Datafilter
        return Datafilter.get_datafilter_by_datafilter_id(self.data_filter_id)

    @classmethod
    def get_cache_chart_by_cache_chart_id(cls, cache_chart_id):
        return cls.select(id=cache_chart_id)

