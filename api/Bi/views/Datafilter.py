# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Datafilter import Datafilter

log = getLogger("views/Datafilter")


class DatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datafilter_id=None):
        if datafilter_id:
            datafilter = Datafilter.select(id=datafilter_id)
            return SuccessData(
                datafilter.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            datafilter_list = Datafilter.search(**search_params).order_by()
            pager = Page(datafilter_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, datafilter_id=None):
        if datafilter_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['column_id'] = self.get_argument('column_id', undefined)
            params['worktable_id'] = self.get_argument('worktable_id', undefined)
            params['dtype'] = self.get_argument('dtype', undefined)
            params['custom_attr'] = self.get_argument('custom_attr', undefined)
            datafilter = Datafilter.select(id=datafilter_id)
            datafilter = datafilter.copy(**params)
            return SuccessData(
                datafilter.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['column_id'] = self.get_argument('column_id', None)
            params['worktable_id'] = self.get_argument('worktable_id', None)
            params['dtype'] = self.get_argument('dtype', None)
            params['custom_attr'] = self.get_argument('custom_attr', None)
            datafilter = Datafilter.create(**params)
            return SuccessData(
                datafilter.id
            )

    @BaseHandler.ajax_base()
    def put(self, datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['column_id'] = self.get_argument('column_id', None)
        params['worktable_id'] = self.get_argument('worktable_id', None)
        params['dtype'] = self.get_argument('dtype', None)
        params['custom_attr'] = self.get_argument('custom_attr', None)
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter = datafilter.update(**params)
        return SuccessData(
            datafilter.id
        )

    @BaseHandler.ajax_base()
    def patch(self, datafilter_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['column_id'] = self.get_argument('column_id', undefined)
        params['worktable_id'] = self.get_argument('worktable_id', undefined)
        params['dtype'] = self.get_argument('dtype', undefined)
        params['custom_attr'] = self.get_argument('custom_attr', undefined)
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter = datafilter.update(**params)
        return SuccessData(
            datafilter.id
        )

    @BaseHandler.ajax_base()
    def delete(self, datafilter_id=None):
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
