# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.DatasourceMerged import DatasourceMerged

log = getLogger("views/DatasourceMerged")


class DatasourceMergedHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_merged_id=None):
        if datasource_merged_id:
            datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
            return SuccessData(
                datasource_merged.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            datasource_merged_list = DatasourceMerged.search(**search_params).order_by()
            pager = Page(datasource_merged_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, datasource_merged_id=None):
        if datasource_merged_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['datamerge_id'] = self.get_argument('datamerge_id', undefined)
            datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
            datasource_merged = datasource_merged.copy(**params)
            return SuccessData(
                datasource_merged.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['datamerge_id'] = self.get_argument('datamerge_id', None)
            datasource_merged = DatasourceMerged.create(**params)
            return SuccessData(
                datasource_merged.id
            )

    @BaseHandler.ajax_base()
    def put(self, datasource_merged_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['datamerge_id'] = self.get_argument('datamerge_id', None)
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged = datasource_merged.update(**params)
        return SuccessData(
            datasource_merged.id
        )

    @BaseHandler.ajax_base()
    def patch(self, datasource_merged_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['datamerge_id'] = self.get_argument('datamerge_id', undefined)
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged = datasource_merged.update(**params)
        return SuccessData(
            datasource_merged.id
        )

    @BaseHandler.ajax_base()
    def delete(self, datasource_merged_id=None):
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
