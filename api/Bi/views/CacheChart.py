# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.CacheChart import CacheChart
from common.Utils.log_utils import getLogger

log = getLogger("views/CacheChart")


class CacheChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, cache_chart_id=None):
        if cache_chart_id:
            cache_chart = CacheChart.select(id=cache_chart_id)
            return CacheChart.to_front()
        else:
            cache_chart_list = CacheChart.filter()
            return [cache_chart.to_front() for cache_chart in cache_chart_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        cache_chart = CacheChart.create(params)
        return cache_chart.to_front()

    @BaseHandler.ajax_base()
    def put(self, cache_chart_id):
        params = self.get_all_arguments()
        cache_chart = CacheChart.select(id=cache_chart_id)
        cache_chart = cache_chart.update(params)
        return cache_chart.to_front()

    @BaseHandler.ajax_base()
    def patch(self, cache_chart_id):
        params = self.get_all_arguments()
        cache_chart = CacheChart.select(id=cache_chart_id)
        cache_chart = cache_chart.update(params)
        return cache_chart.to_front()

    @BaseHandler.ajax_base()
    def delete(self, cache_chart_id):
        cache_chart = CacheChart.select(id=cache_chart_id)
        cache_chart.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
