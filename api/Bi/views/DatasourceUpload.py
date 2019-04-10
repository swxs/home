# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.DatasourceUpload import DatasourceUpload

log = getLogger("views/DatasourceUpload")


class DatasourceUploadHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_upload_id=None):
        if datasource_upload_id:
            datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
            return datasource_upload.to_front()
        else:
            datasource_upload_list = DatasourceUpload.filter()
            return [datasource_upload.to_front() for datasource_upload in datasource_upload_list]

    @BaseHandler.ajax_base()
    def post(self, datasource_upload_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['filename'] = self.get_argument('filename', None)
        datasource_upload = DatasourceUpload.create(**params)
        return datasource_upload.id

    @BaseHandler.ajax_base()
    def put(self, datasource_upload_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['filename'] = self.get_argument('filename', None)
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload = datasource_upload.update(**params)
        return datasource_upload.id

    @BaseHandler.ajax_base()
    def patch(self, datasource_upload_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['filename'] = self.get_argument('filename', undefined)
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload = datasource_upload.update(**params)
        return datasource_upload.id

    @BaseHandler.ajax_base()
    def delete(self, datasource_upload_id=None):
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
