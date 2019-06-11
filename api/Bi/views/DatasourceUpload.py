# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model

import json
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.DatasourceUpload import DatasourceUpload

log = getLogger("views/DatasourceUpload")


class DatasourceUploadHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_upload_id=None):
        if datasource_upload_id:
            datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
            return SuccessData(
                datasource_upload.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            pager = self.get_argument("pager", 1)
            datasource_upload_list = DatasourceUpload.search(**search_params).order_by()
            pager = Page(datasource_upload_list, pager=pager, page=page, items_per_page=items_per_page)
            return SuccessData(
                [item.to_front() for item in pager.items],
                info=pager.info,
            )

    @BaseHandler.ajax_base()
    def post(self, datasource_upload_id=None):
        if datasource_upload_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['filename'] = self.get_argument('filename', undefined)
            datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
            datasource_upload = datasource_upload.copy(**params)
            return SuccessData(
                datasource_upload.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['filename'] = self.get_argument('filename', None)
            datasource_upload = DatasourceUpload.create(**params)
            return SuccessData(
                datasource_upload.id
            )

    @BaseHandler.ajax_base()
    def put(self, datasource_upload_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['filename'] = self.get_argument('filename', None)
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload = datasource_upload.update(**params)
        return SuccessData(
            datasource_upload.id
        )

    @BaseHandler.ajax_base()
    def patch(self, datasource_upload_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['filename'] = self.get_argument('filename', undefined)
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload = datasource_upload.update(**params)
        return SuccessData(
            datasource_upload.id
        )

    @BaseHandler.ajax_base()
    def delete(self, datasource_upload_id=None):
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
