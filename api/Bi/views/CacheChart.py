# -*- coding: utf-8 -*-
# @File    : CacheChart.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.CacheChart import CacheChart

log = getLogger("views/CacheChart")


class CacheChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, cache_chart_id=None):
        if cache_chart_id:
            cache_chart = await CacheChart.select(id=cache_chart_id)
            return SuccessData(
                await cache_chart.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            cache_chart_cursor = CacheChart.search(**search_params)
            data = []
            async for cache_chart in cache_chart_cursor:
                data.append(await cache_chart.to_front())
            return SuccessData(data)
            # pager = Page(cache_chart_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, cache_chart_id=None):
        if cache_chart_id:
            params = dict()
            params['chart_id'] = self.get_argument('chart_id', undefined)
            params['data_filter_id'] = self.get_argument('data_filter_id', undefined)
            params['ttype'] = self.get_argument('ttype', undefined)
            params['key'] = self.get_argument('key', undefined)
            params['value'] = self.get_argument('value', undefined)
            params['status'] = self.get_argument('status', undefined)
            cache_chart = await CacheChart.select(id=cache_chart_id)
            cache_chart = await cache_chart.copy(**params)
            return SuccessData(
                cache_chart.id
            )
        else:
            params = dict()
            params['chart_id'] = self.get_argument('chart_id', None)
            params['data_filter_id'] = self.get_argument('data_filter_id', None)
            params['ttype'] = self.get_argument('ttype', None)
            params['key'] = self.get_argument('key', None)
            params['value'] = self.get_argument('value', None)
            params['status'] = self.get_argument('status', None)
            cache_chart = await CacheChart.create(**params)
            return SuccessData(
                cache_chart.id
            )

    @BaseHandler.ajax_base()
    async def put(self, cache_chart_id=None):
        params = dict()
        params['chart_id'] = self.get_argument('chart_id', None)
        params['data_filter_id'] = self.get_argument('data_filter_id', None)
        params['ttype'] = self.get_argument('ttype', None)
        params['key'] = self.get_argument('key', None)
        params['value'] = self.get_argument('value', None)
        params['status'] = self.get_argument('status', None)
        cache_chart = await CacheChart.select(id=cache_chart_id)
        cache_chart = await cache_chart.update(**params)
        return SuccessData(
            cache_chart.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, cache_chart_id=None):
        params = dict()
        params['chart_id'] = self.get_argument('chart_id', undefined)
        params['data_filter_id'] = self.get_argument('data_filter_id', undefined)
        params['ttype'] = self.get_argument('ttype', undefined)
        params['key'] = self.get_argument('key', undefined)
        params['value'] = self.get_argument('value', undefined)
        params['status'] = self.get_argument('status', undefined)
        cache_chart = await CacheChart.select(id=cache_chart_id)
        cache_chart = await cache_chart.update(**params)
        return SuccessData(
            cache_chart.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, cache_chart_id=None):
        cache_chart = await CacheChart.select(id=cache_chart_id)
        await cache_chart.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
