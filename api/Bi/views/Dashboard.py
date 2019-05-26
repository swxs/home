# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Dashboard import Dashboard

log = getLogger("views/Dashboard")


class DashboardHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, dashboard_id=None):
        if dashboard_id:
            dashboard = Dashboard.select(id=dashboard_id)
            return dashboard.to_front()
        else:
            dashboard_list = Dashboard.filter()
            return [dashboard.to_front() for dashboard in dashboard_list]

    @BaseHandler.ajax_base()
    def post(self, dashboard_id=None):
        if dashboard_id:
            params = dict()
            params['user_id'] = self.get_argument('user_id', undefined)
            params['usage'] = self.get_argument('usage', undefined)
            params['container_id'] = self.get_argument('container_id', undefined)
            params['worktable_id'] = self.get_argument('worktable_id', undefined)
            params['index'] = self.get_argument('index', undefined)
            params['name'] = self.get_argument('name', undefined)
            params['description'] = self.get_argument('description', undefined)
            params['simulate_region_id'] = self.get_argument('simulate_region_id', undefined)
            params['parent_id'] = self.get_argument('parent_id', undefined)
            dashboard = Dashboard.select(id=dashboard_id)
            dashboard = dashboard.copy(**params)
            return dashboard.id
        else:
            params = dict()
            params['user_id'] = self.get_argument('user_id', None)
            params['usage'] = self.get_argument('usage', None)
            params['container_id'] = self.get_argument('container_id', None)
            params['worktable_id'] = self.get_argument('worktable_id', None)
            params['index'] = self.get_argument('index', None)
            params['name'] = self.get_argument('name', None)
            params['description'] = self.get_argument('description', None)
            params['simulate_region_id'] = self.get_argument('simulate_region_id', None)
            params['parent_id'] = self.get_argument('parent_id', None)
            dashboard = Dashboard.create(**params)
            return dashboard.id

    @BaseHandler.ajax_base()
    def put(self, dashboard_id=None):
        params = dict()
        params['user_id'] = self.get_argument('user_id', None)
        params['usage'] = self.get_argument('usage', None)
        params['container_id'] = self.get_argument('container_id', None)
        params['worktable_id'] = self.get_argument('worktable_id', None)
        params['index'] = self.get_argument('index', None)
        params['name'] = self.get_argument('name', None)
        params['description'] = self.get_argument('description', None)
        params['simulate_region_id'] = self.get_argument('simulate_region_id', None)
        params['parent_id'] = self.get_argument('parent_id', None)
        dashboard = Dashboard.select(id=dashboard_id)
        dashboard = dashboard.update(**params)
        return dashboard.id

    @BaseHandler.ajax_base()
    def patch(self, dashboard_id=None):
        params = dict()
        params['user_id'] = self.get_argument('user_id', undefined)
        params['usage'] = self.get_argument('usage', undefined)
        params['container_id'] = self.get_argument('container_id', undefined)
        params['worktable_id'] = self.get_argument('worktable_id', undefined)
        params['index'] = self.get_argument('index', undefined)
        params['name'] = self.get_argument('name', undefined)
        params['description'] = self.get_argument('description', undefined)
        params['simulate_region_id'] = self.get_argument('simulate_region_id', undefined)
        params['parent_id'] = self.get_argument('parent_id', undefined)
        dashboard = Dashboard.select(id=dashboard_id)
        dashboard = dashboard.update(**params)
        return dashboard.id

    @BaseHandler.ajax_base()
    def delete(self, dashboard_id=None):
        dashboard = Dashboard.select(id=dashboard_id)
        dashboard.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
