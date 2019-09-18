# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.DatasourceMerged import DatasourceMerged

log = getLogger("views/DatasourceMerged")


class DatasourceMergedHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, datasource_merged_id=None):
        if datasource_merged_id:
            datasource_merged = await DatasourceMerged.select(id=datasource_merged_id)
            return SuccessData(
                await datasource_merged.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            datasource_merged_cursor = DatasourceMerged.search(**search_params)
            data = []
            async for datasource_merged in datasource_merged_cursor:
                data.append(await datasource_merged.to_front())
            return SuccessData(data)
            # pager = Page(datasource_merged_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, datasource_merged_id=None):
        if datasource_merged_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['datamerge_id'] = self.get_argument('datamerge_id', undefined)
            datasource_merged = await DatasourceMerged.select(id=datasource_merged_id)
            datasource_merged = await datasource_merged.copy(**params)
            return SuccessData(
                datasource_merged.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['datamerge_id'] = self.get_argument('datamerge_id', None)
            datasource_merged = await DatasourceMerged.create(**params)
            return SuccessData(
                datasource_merged.id
            )

    @BaseHandler.ajax_base()
    async def put(self, datasource_merged_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['datamerge_id'] = self.get_argument('datamerge_id', None)
        datasource_merged = await DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged = await datasource_merged.update(**params)
        return SuccessData(
            datasource_merged.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, datasource_merged_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['datamerge_id'] = self.get_argument('datamerge_id', undefined)
        datasource_merged = await DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged = await datasource_merged.update(**params)
        return SuccessData(
            datasource_merged.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, datasource_merged_id=None):
        datasource_merged = await DatasourceMerged.select(id=datasource_merged_id)
        await datasource_merged.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
