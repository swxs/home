# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Datamerge import Datamerge

log = getLogger("views/Datamerge")


class DatamergeHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, datamerge_id=None):
        if datamerge_id:
            datamerge = await Datamerge.select(id=datamerge_id)
            return SuccessData(
                await datamerge.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            datamerge_cursor = Datamerge.search(**search_params)
            data = []
            async for datamerge in datamerge_cursor:
                data.append(await datamerge.to_front())
            return SuccessData(data)
            # pager = Page(datamerge_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, datamerge_id=None):
        if datamerge_id:
            params = dict()
            params['source_worktable_id'] = self.get_argument('source_worktable_id', undefined)
            params['source_column_id_list'] = self.get_arguments('source_column_id_list', undefined)
            params['remote_worktable_id'] = self.get_argument('remote_worktable_id', undefined)
            params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', undefined)
            params['how'] = self.get_argument('how', undefined)
            datamerge = await Datamerge.select(id=datamerge_id)
            datamerge = await datamerge.copy(**params)
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
            datamerge = await Datamerge.create(**params)
            return SuccessData(
                datamerge.id
            )

    @BaseHandler.ajax_base()
    async def put(self, datamerge_id=None):
        params = dict()
        params['source_worktable_id'] = self.get_argument('source_worktable_id', None)
        params['source_column_id_list'] = self.get_arguments('source_column_id_list', [])
        params['remote_worktable_id'] = self.get_argument('remote_worktable_id', None)
        params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', [])
        params['how'] = self.get_argument('how', None)
        datamerge = await Datamerge.select(id=datamerge_id)
        datamerge = await datamerge.update(**params)
        return SuccessData(
            datamerge.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, datamerge_id=None):
        params = dict()
        params['source_worktable_id'] = self.get_argument('source_worktable_id', undefined)
        params['source_column_id_list'] = self.get_arguments('source_column_id_list', undefined)
        params['remote_worktable_id'] = self.get_argument('remote_worktable_id', undefined)
        params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', undefined)
        params['how'] = self.get_argument('how', undefined)
        datamerge = await Datamerge.select(id=datamerge_id)
        datamerge = await datamerge.update(**params)
        return SuccessData(
            datamerge.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, datamerge_id=None):
        datamerge = await Datamerge.select(id=datamerge_id)
        await datamerge.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
