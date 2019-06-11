# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Datasource import Datasource

log = getLogger("views/Datasource")


class DatasourceHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_id=None):
        if datasource_id:
            datasource = Datasource.select(id=datasource_id)
            return SuccessData(
                datasource.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            datasource_list = Datasource.search(**search_params).order_by()
            pager = Page(datasource_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, datasource_id=None):
        if datasource_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            datasource = Datasource.select(id=datasource_id)
            datasource = datasource.copy(**params)
            return SuccessData(
                datasource.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            datasource = Datasource.create(**params)
            return SuccessData(
                datasource.id
            )

    @BaseHandler.ajax_base()
    def put(self, datasource_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        datasource = Datasource.select(id=datasource_id)
        datasource = datasource.update(**params)
        return SuccessData(
            datasource.id
        )

    @BaseHandler.ajax_base()
    def patch(self, datasource_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        datasource = Datasource.select(id=datasource_id)
        datasource = datasource.update(**params)
        return SuccessData(
            datasource.id
        )

    @BaseHandler.ajax_base()
    def delete(self, datasource_id=None):
        datasource = Datasource.select(id=datasource_id)
        datasource.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
