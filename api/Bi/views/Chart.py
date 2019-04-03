# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Chart import Chart
from common.Utils.log_utils import getLogger

log = getLogger("views/Chart")


class ChartHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, chart_id=None):
        if chart_id:
            chart = Chart.select(id=chart_id)
            return Chart.to_front()
        else:
            chart_list = Chart.filter()
            return [chart.to_front() for chart in chart_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        chart = Chart.create(params)
        return chart.to_front()

    @BaseHandler.ajax_base()
    def put(self, chart_id):
        params = self.get_all_arguments()
        chart = Chart.select(id=chart_id)
        chart = chart.update(params)
        return chart.to_front()

    @BaseHandler.ajax_base()
    def patch(self, chart_id):
        params = self.get_all_arguments()
        chart = Chart.select(id=chart_id)
        chart = chart.update(params)
        return chart.to_front()

    @BaseHandler.ajax_base()
    def delete(self, chart_id):
        chart = Chart.select(id=chart_id)
        chart.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
