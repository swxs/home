# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.ContainerChart import ContainerChart

log = getLogger("views/ContainerChart")


class ContainerChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_chart_id=None):
        if container_chart_id:
            container_chart = ContainerChart.select(id=container_chart_id)
            return SuccessData(
                container_chart.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            container_chart_list = ContainerChart.search(**search_params).order_by()
            pager = Page(container_chart_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, container_chart_id=None):
        if container_chart_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['show_name'] = self.get_argument('show_name', undefined)
            params['chart_id'] = self.get_argument('chart_id', undefined)
            container_chart = ContainerChart.select(id=container_chart_id)
            container_chart = container_chart.copy(**params)
            return SuccessData(
                container_chart.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['show_name'] = self.get_argument('show_name', None)
            params['chart_id'] = self.get_argument('chart_id', None)
            container_chart = ContainerChart.create(**params)
            return SuccessData(
                container_chart.id
            )

    @BaseHandler.ajax_base()
    def put(self, container_chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['chart_id'] = self.get_argument('chart_id', None)
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart = container_chart.update(**params)
        return SuccessData(
            container_chart.id
        )

    @BaseHandler.ajax_base()
    def patch(self, container_chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['chart_id'] = self.get_argument('chart_id', undefined)
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart = container_chart.update(**params)
        return SuccessData(
            container_chart.id
        )

    @BaseHandler.ajax_base()
    def delete(self, container_chart_id=None):
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
