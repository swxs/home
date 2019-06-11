# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.DatasourceRegion import DatasourceRegion

log = getLogger("views/DatasourceRegion")


class DatasourceRegionHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_region_id=None):
        if datasource_region_id:
            datasource_region = DatasourceRegion.select(id=datasource_region_id)
            return SuccessData(
                datasource_region.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            datasource_region_list = DatasourceRegion.search(**search_params).order_by()
            pager = Page(datasource_region_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, datasource_region_id=None):
        if datasource_region_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['region_type_id'] = self.get_argument('region_type_id', undefined)
            datasource_region = DatasourceRegion.select(id=datasource_region_id)
            datasource_region = datasource_region.copy(**params)
            return SuccessData(
                datasource_region.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['region_type_id'] = self.get_argument('region_type_id', None)
            datasource_region = DatasourceRegion.create(**params)
            return SuccessData(
                datasource_region.id
            )

    @BaseHandler.ajax_base()
    def put(self, datasource_region_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['region_type_id'] = self.get_argument('region_type_id', None)
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region = datasource_region.update(**params)
        return SuccessData(
            datasource_region.id
        )

    @BaseHandler.ajax_base()
    def patch(self, datasource_region_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['region_type_id'] = self.get_argument('region_type_id', undefined)
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region = datasource_region.update(**params)
        return SuccessData(
            datasource_region.id
        )

    @BaseHandler.ajax_base()
    def delete(self, datasource_region_id=None):
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
