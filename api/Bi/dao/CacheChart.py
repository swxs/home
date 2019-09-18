# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.CacheChart import CacheChart as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class CacheChart(BaseDAO):
    chart_id = model.ObjectIdField()
    data_filter_id = model.ObjectIdField()
    ttype = model.IntField()
    key = model.StringField()
    value = model.StringField()
    status = model.IntField()

    def __init__(self, **kwargs):
        super(CacheChart, self).__init__(**kwargs)

    @async_property
    async def chart(self):
        from .Chart import Chart
        return await Chart.get_chart_by_chart_id(self.chart_id)

    @async_property
    async def datafilter(self):
        from .Datafilter import Datafilter
        return await Datafilter.get_datafilter_by_datafilter_id(self.data_filter_id)

    @classmethod
    async def get_cache_chart_by_cache_chart_id(cls, cache_chart_id):
        return await cls.select(id=cache_chart_id)

