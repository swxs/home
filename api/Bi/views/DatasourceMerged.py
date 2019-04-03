# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.DatasourceMerged import DatasourceMerged
from common.Utils.log_utils import getLogger

log = getLogger("views/DatasourceMerged")


class DatasourceMergedHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_merged_id=None):
        if datasource_merged_id:
            datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
            return DatasourceMerged.to_front()
        else:
            datasource_merged_list = DatasourceMerged.filter()
            return [datasource_merged.to_front() for datasource_merged in datasource_merged_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        datasource_merged = DatasourceMerged.create(params)
        return datasource_merged.to_front()

    @BaseHandler.ajax_base()
    def put(self, datasource_merged_id):
        params = self.get_all_arguments()
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged = datasource_merged.update(params)
        return datasource_merged.to_front()

    @BaseHandler.ajax_base()
    def patch(self, datasource_merged_id):
        params = self.get_all_arguments()
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged = datasource_merged.update(params)
        return datasource_merged.to_front()

    @BaseHandler.ajax_base()
    def delete(self, datasource_merged_id):
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
