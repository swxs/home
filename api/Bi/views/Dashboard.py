# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Dashboard import Dashboard

log = getLogger("views/Dashboard")


class DashboardHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, dashboard_id=None):
        if dashboard_id:
            dashboard = Dashboard.select(id=dashboard_id)
            return SuccessData(
                dashboard.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            dashboard_list = Dashboard.search(**search_params).order_by()
            pager = Page(dashboard_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

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
            return SuccessData(
                dashboard.id
            )
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
            return SuccessData(
                dashboard.id
            )

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
        return SuccessData(
            dashboard.id
        )

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
        return SuccessData(
            dashboard.id
        )

    @BaseHandler.ajax_base()
    def delete(self, dashboard_id=None):
        dashboard = Dashboard.select(id=dashboard_id)
        dashboard.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
