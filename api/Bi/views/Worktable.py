# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Worktable import Worktable

log = getLogger("views/Worktable")


class WorktableHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, worktable_id=None):
        if worktable_id:
            worktable = Worktable.select(id=worktable_id)
            return SuccessData(
                worktable.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            worktable_list = Worktable.search(**search_params).order_by()
            pager = Page(worktable_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, worktable_id=None):
        if worktable_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['datasource_id'] = self.get_argument('datasource_id', undefined)
            params['engine'] = self.get_argument('engine', undefined)
            params['status'] = self.get_argument('status', undefined)
            params['description'] = self.get_argument('description', undefined)
            worktable = Worktable.select(id=worktable_id)
            worktable = worktable.copy(**params)
            return SuccessData(
                worktable.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['datasource_id'] = self.get_argument('datasource_id', None)
            params['engine'] = self.get_argument('engine', None)
            params['status'] = self.get_argument('status', None)
            params['description'] = self.get_argument('description', None)
            worktable = Worktable.create(**params)
            return SuccessData(
                worktable.id
            )

    @BaseHandler.ajax_base()
    def put(self, worktable_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['datasource_id'] = self.get_argument('datasource_id', None)
        params['engine'] = self.get_argument('engine', None)
        params['status'] = self.get_argument('status', None)
        params['description'] = self.get_argument('description', None)
        worktable = Worktable.select(id=worktable_id)
        worktable = worktable.update(**params)
        return SuccessData(
            worktable.id
        )

    @BaseHandler.ajax_base()
    def patch(self, worktable_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['datasource_id'] = self.get_argument('datasource_id', undefined)
        params['engine'] = self.get_argument('engine', undefined)
        params['status'] = self.get_argument('status', undefined)
        params['description'] = self.get_argument('description', undefined)
        worktable = Worktable.select(id=worktable_id)
        worktable = worktable.update(**params)
        return SuccessData(
            worktable.id
        )

    @BaseHandler.ajax_base()
    def delete(self, worktable_id=None):
        worktable = Worktable.select(id=worktable_id)
        worktable.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
