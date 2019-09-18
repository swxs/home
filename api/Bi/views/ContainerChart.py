# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.ContainerChart import ContainerChart

log = getLogger("views/ContainerChart")


class ContainerChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, container_chart_id=None):
        if container_chart_id:
            container_chart = await ContainerChart.select(id=container_chart_id)
            return SuccessData(
                await container_chart.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            container_chart_cursor = ContainerChart.search(**search_params)
            data = []
            async for container_chart in container_chart_cursor:
                data.append(await container_chart.to_front())
            return SuccessData(data)
            # pager = Page(container_chart_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, container_chart_id=None):
        if container_chart_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            params['chart_id'] = self.get_argument('chart_id', undefined)
            container_chart = await ContainerChart.select(id=container_chart_id)
            container_chart = await container_chart.copy(**params)
            return SuccessData(
                container_chart.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            params['chart_id'] = self.get_argument('chart_id', None)
            container_chart = await ContainerChart.create(**params)
            return SuccessData(
                container_chart.id
            )

    @BaseHandler.ajax_base()
    async def put(self, container_chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['chart_id'] = self.get_argument('chart_id', None)
        container_chart = await ContainerChart.select(id=container_chart_id)
        container_chart = await container_chart.update(**params)
        return SuccessData(
            container_chart.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, container_chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['chart_id'] = self.get_argument('chart_id', undefined)
        container_chart = await ContainerChart.select(id=container_chart_id)
        container_chart = await container_chart.update(**params)
        return SuccessData(
            container_chart.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, container_chart_id=None):
        container_chart = await ContainerChart.select(id=container_chart_id)
        await container_chart.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
