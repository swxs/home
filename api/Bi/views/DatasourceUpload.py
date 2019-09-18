# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.DatasourceUpload import DatasourceUpload

log = getLogger("views/DatasourceUpload")


class DatasourceUploadHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, datasource_upload_id=None):
        if datasource_upload_id:
            datasource_upload = await DatasourceUpload.select(id=datasource_upload_id)
            return SuccessData(
                await datasource_upload.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            datasource_upload_cursor = DatasourceUpload.search(**search_params)
            data = []
            async for datasource_upload in datasource_upload_cursor:
                data.append(await datasource_upload.to_front())
            return SuccessData(data)
            # pager = Page(datasource_upload_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, datasource_upload_id=None):
        if datasource_upload_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['filename'] = self.get_argument('filename', undefined)
            datasource_upload = await DatasourceUpload.select(id=datasource_upload_id)
            datasource_upload = await datasource_upload.copy(**params)
            return SuccessData(
                datasource_upload.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['filename'] = self.get_argument('filename', None)
            datasource_upload = await DatasourceUpload.create(**params)
            return SuccessData(
                datasource_upload.id
            )

    @BaseHandler.ajax_base()
    async def put(self, datasource_upload_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['filename'] = self.get_argument('filename', None)
        datasource_upload = await DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload = await datasource_upload.update(**params)
        return SuccessData(
            datasource_upload.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, datasource_upload_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['filename'] = self.get_argument('filename', undefined)
        datasource_upload = await DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload = await datasource_upload.update(**params)
        return SuccessData(
            datasource_upload.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, datasource_upload_id=None):
        datasource_upload = await DatasourceUpload.select(id=datasource_upload_id)
        await datasource_upload.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
