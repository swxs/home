# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : DatasourceUpload.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.DatasourceUpload import DatasourceUpload
from common.Utils.log_utils import getLogger

log = getLogger("views/DatasourceUpload")


class DatasourceUploadHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_upload_id=None):
        if datasource_upload_id:
            datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
            return DatasourceUpload.to_front()
        else:
            datasource_upload_list = DatasourceUpload.filter()
            return [datasource_upload.to_front() for datasource_upload in datasource_upload_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        datasource_upload = DatasourceUpload.create(params)
        return datasource_upload.to_front()

    @BaseHandler.ajax_base()
    def put(self, datasource_upload_id):
        params = self.get_all_arguments()
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload = datasource_upload.update(params)
        return datasource_upload.to_front()

    @BaseHandler.ajax_base()
    def patch(self, datasource_upload_id):
        params = self.get_all_arguments()
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload = datasource_upload.update(params)
        return datasource_upload.to_front()

    @BaseHandler.ajax_base()
    def delete(self, datasource_upload_id):
        datasource_upload = DatasourceUpload.select(id=datasource_upload_id)
        datasource_upload.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
