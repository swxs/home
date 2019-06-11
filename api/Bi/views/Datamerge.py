# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Datamerge import Datamerge

log = getLogger("views/Datamerge")


class DatamergeHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datamerge_id=None):
        if datamerge_id:
            datamerge = Datamerge.select(id=datamerge_id)
            return SuccessData(
                datamerge.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            datamerge_list = Datamerge.search(**search_params).order_by()
            pager = Page(datamerge_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, datamerge_id=None):
        if datamerge_id:
            params = dict()
            params['source_worktable_id'] = self.get_argument('source_worktable_id', undefined)
            params['source_column_id_list'] = self.get_arguments('source_column_id_list', undefined)
            params['remote_worktable_id'] = self.get_argument('remote_worktable_id', undefined)
            params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', undefined)
            params['how'] = self.get_argument('how', undefined)
            datamerge = Datamerge.select(id=datamerge_id)
            datamerge = datamerge.copy(**params)
            return SuccessData(
                datamerge.id
            )
        else:
            params = dict()
            params['source_worktable_id'] = self.get_argument('source_worktable_id', None)
            params['source_column_id_list'] = self.get_arguments('source_column_id_list', [])
            params['remote_worktable_id'] = self.get_argument('remote_worktable_id', None)
            params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', [])
            params['how'] = self.get_argument('how', None)
            datamerge = Datamerge.create(**params)
            return SuccessData(
                datamerge.id
            )

    @BaseHandler.ajax_base()
    def put(self, datamerge_id=None):
        params = dict()
        params['source_worktable_id'] = self.get_argument('source_worktable_id', None)
        params['source_column_id_list'] = self.get_arguments('source_column_id_list', [])
        params['remote_worktable_id'] = self.get_argument('remote_worktable_id', None)
        params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', [])
        params['how'] = self.get_argument('how', None)
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge = datamerge.update(**params)
        return SuccessData(
            datamerge.id
        )

    @BaseHandler.ajax_base()
    def patch(self, datamerge_id=None):
        params = dict()
        params['source_worktable_id'] = self.get_argument('source_worktable_id', undefined)
        params['source_column_id_list'] = self.get_arguments('source_column_id_list', undefined)
        params['remote_worktable_id'] = self.get_argument('remote_worktable_id', undefined)
        params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', undefined)
        params['how'] = self.get_argument('how', undefined)
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge = datamerge.update(**params)
        return SuccessData(
            datamerge.id
        )

    @BaseHandler.ajax_base()
    def delete(self, datamerge_id=None):
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
