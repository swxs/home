# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.DatasourceRegion import DatasourceRegion

log = getLogger("views/DatasourceRegion")


class DatasourceRegionHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_region_id=None):
        if datasource_region_id:
            datasource_region = DatasourceRegion.select(id=datasource_region_id)
            return datasource_region.to_front()
        else:
            datasource_region_list = DatasourceRegion.filter()
            return [datasource_region.to_front() for datasource_region in datasource_region_list]

    @BaseHandler.ajax_base()
    def post(self, datasource_region_id=None):
        if datasource_region_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['region_type_id'] = self.get_argument('region_type_id', undefined)
            datasource_region = DatasourceRegion.select(id=datasource_region_id)
            datasource_region = datasource_region.copy(**params)
            return datasource_region.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['region_type_id'] = self.get_argument('region_type_id', None)
            datasource_region = DatasourceRegion.create(**params)
            return datasource_region.id

    @BaseHandler.ajax_base()
    def put(self, datasource_region_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['region_type_id'] = self.get_argument('region_type_id', None)
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region = datasource_region.update(**params)
        return datasource_region.id

    @BaseHandler.ajax_base()
    def patch(self, datasource_region_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['region_type_id'] = self.get_argument('region_type_id', undefined)
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region = datasource_region.update(**params)
        return datasource_region.id

    @BaseHandler.ajax_base()
    def delete(self, datasource_region_id=None):
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
