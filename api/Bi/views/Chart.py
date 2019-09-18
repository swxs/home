# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Chart import Chart

log = getLogger("views/Chart")


class ChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, chart_id=None):
        if chart_id:
            chart = await Chart.select(id=chart_id)
            return SuccessData(
                await chart.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            chart_cursor = Chart.search(**search_params)
            data = []
            async for chart in chart_cursor:
                data.append(await chart.to_front())
            return SuccessData(data)
            # pager = Page(chart_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, chart_id=None):
        if chart_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['title'] = self.get_argument('title', undefined)
            params['worktable_id'] = self.get_argument('worktable_id', undefined)
            params['is_drilldown'] = self.get_argument('is_drilldown', undefined)
            params['ttype'] = self.get_argument('ttype', undefined)
            params['range_region_type_id'] = self.get_argument('range_region_type_id', undefined)
            params['base_option'] = self.get_argument('base_option', undefined)
            params['next_chart_id'] = self.get_argument('next_chart_id', undefined)
            params['prev_chart_id'] = self.get_argument('prev_chart_id', undefined)
            params['custom_attr'] = self.get_argument('custom_attr', undefined)
            params['markline'] = self.get_arguments('markline', undefined)
            chart = await Chart.select(id=chart_id)
            chart = await chart.copy(**params)
            return SuccessData(
                chart.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['title'] = self.get_argument('title', None)
            params['worktable_id'] = self.get_argument('worktable_id', None)
            params['is_drilldown'] = self.get_argument('is_drilldown', None)
            params['ttype'] = self.get_argument('ttype', None)
            params['range_region_type_id'] = self.get_argument('range_region_type_id', None)
            params['base_option'] = self.get_argument('base_option', None)
            params['next_chart_id'] = self.get_argument('next_chart_id', None)
            params['prev_chart_id'] = self.get_argument('prev_chart_id', None)
            params['custom_attr'] = self.get_argument('custom_attr', None)
            params['markline'] = self.get_arguments('markline', [])
            chart = await Chart.create(**params)
            return SuccessData(
                chart.id
            )

    @BaseHandler.ajax_base()
    async def put(self, chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['title'] = self.get_argument('title', None)
        params['worktable_id'] = self.get_argument('worktable_id', None)
        params['is_drilldown'] = self.get_argument('is_drilldown', None)
        params['ttype'] = self.get_argument('ttype', None)
        params['range_region_type_id'] = self.get_argument('range_region_type_id', None)
        params['base_option'] = self.get_argument('base_option', None)
        params['next_chart_id'] = self.get_argument('next_chart_id', None)
        params['prev_chart_id'] = self.get_argument('prev_chart_id', None)
        params['custom_attr'] = self.get_argument('custom_attr', None)
        params['markline'] = self.get_arguments('markline', [])
        chart = await Chart.select(id=chart_id)
        chart = await chart.update(**params)
        return SuccessData(
            chart.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['title'] = self.get_argument('title', undefined)
        params['worktable_id'] = self.get_argument('worktable_id', undefined)
        params['is_drilldown'] = self.get_argument('is_drilldown', undefined)
        params['ttype'] = self.get_argument('ttype', undefined)
        params['range_region_type_id'] = self.get_argument('range_region_type_id', undefined)
        params['base_option'] = self.get_argument('base_option', undefined)
        params['next_chart_id'] = self.get_argument('next_chart_id', undefined)
        params['prev_chart_id'] = self.get_argument('prev_chart_id', undefined)
        params['custom_attr'] = self.get_argument('custom_attr', undefined)
        params['markline'] = self.get_arguments('markline', undefined)
        chart = await Chart.select(id=chart_id)
        chart = await chart.update(**params)
        return SuccessData(
            chart.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, chart_id=None):
        chart = await Chart.select(id=chart_id)
        await chart.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
