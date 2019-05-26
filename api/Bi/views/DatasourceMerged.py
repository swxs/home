# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.DatasourceMerged import DatasourceMerged

log = getLogger("views/DatasourceMerged")


class DatasourceMergedHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_merged_id=None):
        if datasource_merged_id:
            datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
            return datasource_merged.to_front()
        else:
            datasource_merged_list = DatasourceMerged.filter()
            return [datasource_merged.to_front() for datasource_merged in datasource_merged_list]

    @BaseHandler.ajax_base()
    def post(self, datasource_merged_id=None):
        if datasource_merged_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['datamerge_id'] = self.get_argument('datamerge_id', undefined)
            datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
            datasource_merged = datasource_merged.copy(**params)
            return datasource_merged.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['datamerge_id'] = self.get_argument('datamerge_id', None)
            datasource_merged = DatasourceMerged.create(**params)
            return datasource_merged.id

    @BaseHandler.ajax_base()
    def put(self, datasource_merged_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['datamerge_id'] = self.get_argument('datamerge_id', None)
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged = datasource_merged.update(**params)
        return datasource_merged.id

    @BaseHandler.ajax_base()
    def patch(self, datasource_merged_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['datamerge_id'] = self.get_argument('datamerge_id', undefined)
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged = datasource_merged.update(**params)
        return datasource_merged.id

    @BaseHandler.ajax_base()
    def delete(self, datasource_merged_id=None):
        datasource_merged = DatasourceMerged.select(id=datasource_merged_id)
        datasource_merged.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
