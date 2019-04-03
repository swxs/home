# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Dashboard import Dashboard
from common.Utils.log_utils import getLogger

log = getLogger("views/Dashboard")


class DashboardHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, dashboard_id=None):
        if dashboard_id:
            dashboard = Dashboard.select(id=dashboard_id)
            return Dashboard.to_front()
        else:
            dashboard_list = Dashboard.filter()
            return [dashboard.to_front() for dashboard in dashboard_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        dashboard = Dashboard.create(params)
        return dashboard.to_front()

    @BaseHandler.ajax_base()
    def put(self, dashboard_id):
        params = self.get_all_arguments()
        dashboard = Dashboard.select(id=dashboard_id)
        dashboard = dashboard.update(params)
        return dashboard.to_front()

    @BaseHandler.ajax_base()
    def patch(self, dashboard_id):
        params = self.get_all_arguments()
        dashboard = Dashboard.select(id=dashboard_id)
        dashboard = dashboard.update(params)
        return dashboard.to_front()

    @BaseHandler.ajax_base()
    def delete(self, dashboard_id):
        dashboard = Dashboard.select(id=dashboard_id)
        dashboard.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
