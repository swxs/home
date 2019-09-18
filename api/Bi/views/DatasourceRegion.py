# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.DatasourceRegion import DatasourceRegion

log = getLogger("views/DatasourceRegion")


class DatasourceRegionHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, datasource_region_id=None):
        if datasource_region_id:
            datasource_region = await DatasourceRegion.select(id=datasource_region_id)
            return SuccessData(
                await datasource_region.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            datasource_region_cursor = DatasourceRegion.search(**search_params)
            data = []
            async for datasource_region in datasource_region_cursor:
                data.append(await datasource_region.to_front())
            return SuccessData(data)
            # pager = Page(datasource_region_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, datasource_region_id=None):
        if datasource_region_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['region_type_id'] = self.get_argument('region_type_id', undefined)
            datasource_region = await DatasourceRegion.select(id=datasource_region_id)
            datasource_region = await datasource_region.copy(**params)
            return SuccessData(
                datasource_region.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['region_type_id'] = self.get_argument('region_type_id', None)
            datasource_region = await DatasourceRegion.create(**params)
            return SuccessData(
                datasource_region.id
            )

    @BaseHandler.ajax_base()
    async def put(self, datasource_region_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['region_type_id'] = self.get_argument('region_type_id', None)
        datasource_region = await DatasourceRegion.select(id=datasource_region_id)
        datasource_region = await datasource_region.update(**params)
        return SuccessData(
            datasource_region.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, datasource_region_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['region_type_id'] = self.get_argument('region_type_id', undefined)
        datasource_region = await DatasourceRegion.select(id=datasource_region_id)
        datasource_region = await datasource_region.update(**params)
        return SuccessData(
            datasource_region.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, datasource_region_id=None):
        datasource_region = await DatasourceRegion.select(id=datasource_region_id)
        await datasource_region.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
