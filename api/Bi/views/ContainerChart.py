# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.ContainerChart import ContainerChart
from common.Utils.log_utils import getLogger

log = getLogger("views/ContainerChart")


class ContainerChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, container_chart_id=None):
        if container_chart_id:
            container_chart = ContainerChart.select(id=container_chart_id)
            return ContainerChart.to_front()
        else:
            container_chart_list = ContainerChart.filter()
            return [container_chart.to_front() for container_chart in container_chart_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        container_chart = ContainerChart.create(params)
        return container_chart.to_front()

    @BaseHandler.ajax_base()
    def put(self, container_chart_id):
        params = self.get_all_arguments()
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart = container_chart.update(params)
        return container_chart.to_front()

    @BaseHandler.ajax_base()
    def patch(self, container_chart_id):
        params = self.get_all_arguments()
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart = container_chart.update(params)
        return container_chart.to_front()

    @BaseHandler.ajax_base()
    def delete(self, container_chart_id):
        container_chart = ContainerChart.select(id=container_chart_id)
        container_chart.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
