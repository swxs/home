# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.CacheChart import CacheChart

log = getLogger("views/CacheChart")


class CacheChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, cache_chart_id=None):
        if cache_chart_id:
            cache_chart = CacheChart.select(id=cache_chart_id)
            return cache_chart.to_front()
        else:
            cache_chart_list = CacheChart.filter()
            return [cache_chart.to_front() for cache_chart in cache_chart_list]

    @BaseHandler.ajax_base()
    def post(self, cache_chart_id=None):
        if cache_chart_id:
            params = dict()
            params['chart_id'] = self.get_argument('chart_id', undefined)
            params['data_filter_id'] = self.get_argument('data_filter_id', undefined)
            params['ttype'] = self.get_argument('ttype', undefined)
            params['key'] = self.get_argument('key', undefined)
            params['value'] = self.get_argument('value', undefined)
            params['status'] = self.get_argument('status', undefined)
            cache_chart = CacheChart.select(id=cache_chart_id)
            cache_chart = cache_chart.copy(**params)
            return cache_chart.id
        else:
            params = dict()
            params['chart_id'] = self.get_argument('chart_id', None)
            params['data_filter_id'] = self.get_argument('data_filter_id', None)
            params['ttype'] = self.get_argument('ttype', None)
            params['key'] = self.get_argument('key', None)
            params['value'] = self.get_argument('value', None)
            params['status'] = self.get_argument('status', None)
            cache_chart = CacheChart.create(**params)
            return cache_chart.id

    @BaseHandler.ajax_base()
    def put(self, cache_chart_id=None):
        params = dict()
        params['chart_id'] = self.get_argument('chart_id', None)
        params['data_filter_id'] = self.get_argument('data_filter_id', None)
        params['ttype'] = self.get_argument('ttype', None)
        params['key'] = self.get_argument('key', None)
        params['value'] = self.get_argument('value', None)
        params['status'] = self.get_argument('status', None)
        cache_chart = CacheChart.select(id=cache_chart_id)
        cache_chart = cache_chart.update(**params)
        return cache_chart.id

    @BaseHandler.ajax_base()
    def patch(self, cache_chart_id=None):
        params = dict()
        params['chart_id'] = self.get_argument('chart_id', undefined)
        params['data_filter_id'] = self.get_argument('data_filter_id', undefined)
        params['ttype'] = self.get_argument('ttype', undefined)
        params['key'] = self.get_argument('key', undefined)
        params['value'] = self.get_argument('value', undefined)
        params['status'] = self.get_argument('status', undefined)
        cache_chart = CacheChart.select(id=cache_chart_id)
        cache_chart = cache_chart.update(**params)
        return cache_chart.id

    @BaseHandler.ajax_base()
    def delete(self, cache_chart_id=None):
        cache_chart = CacheChart.select(id=cache_chart_id)
        cache_chart.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
