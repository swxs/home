# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Datasource import Datasource

log = getLogger("views/Datasource")


class DatasourceHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, datasource_id=None):
        if datasource_id:
            datasource = await Datasource.select(id=datasource_id)
            return SuccessData(
                await datasource.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            datasource_cursor = Datasource.search(**search_params)
            data = []
            async for datasource in datasource_cursor:
                data.append(await datasource.to_front())
            return SuccessData(data)
            # pager = Page(datasource_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, datasource_id=None):
        if datasource_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            datasource = await Datasource.select(id=datasource_id)
            datasource = await datasource.copy(**params)
            return SuccessData(
                datasource.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            datasource = await Datasource.create(**params)
            return SuccessData(
                datasource.id
            )

    @BaseHandler.ajax_base()
    async def put(self, datasource_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        datasource = await Datasource.select(id=datasource_id)
        datasource = await datasource.update(**params)
        return SuccessData(
            datasource.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, datasource_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        datasource = await Datasource.select(id=datasource_id)
        datasource = await datasource.update(**params)
        return SuccessData(
            datasource.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, datasource_id=None):
        datasource = await Datasource.select(id=datasource_id)
        await datasource.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
