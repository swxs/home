# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.ContainerChart import ContainerChart

log = getLogger("views/ContainerChart")


class ContainerChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_chart_id=None):
        if container_chart_id:
            container_chart = ContainerChart.select(id=container_chart_id)
            return container_chart.to_front()
        else:
            container_chart_list = ContainerChart.filter()
            return [container_chart.to_front() for container_chart in container_chart_list]

    @BaseHandler.ajax_base()
    def post(self, container_chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['chart_id'] = self.get_argument('chart_id', None)
        container_chart = ContainerChart.create(**params)
        return container_chart.id

    @BaseHandler.ajax_base()
    def put(self, container_chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['show_name'] = self.get_argument('show_name', None)
        params['chart_id'] = self.get_argument('chart_id', None)
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart = container_chart.update(**params)
        return container_chart.id

    @BaseHandler.ajax_base()
    def patch(self, container_chart_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['show_name'] = self.get_argument('show_name', undefined)
        params['chart_id'] = self.get_argument('chart_id', undefined)
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart = container_chart.update(**params)
        return container_chart.id

    @BaseHandler.ajax_base()
    def delete(self, container_chart_id=None):
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
