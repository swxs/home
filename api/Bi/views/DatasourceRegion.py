# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.DatasourceRegion import DatasourceRegion
from common.Utils.log_utils import getLogger

log = getLogger("views/DatasourceRegion")


class DatasourceRegionHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_region_id=None):
        if datasource_region_id:
            datasource_region = DatasourceRegion.select(id=datasource_region_id)
            return DatasourceRegion.to_front()
        else:
            datasource_region_list = DatasourceRegion.filter()
            return [datasource_region.to_front() for datasource_region in datasource_region_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        datasource_region = DatasourceRegion.create(params)
        return datasource_region.to_front()

    @BaseHandler.ajax_base()
    def put(self, datasource_region_id):
        params = self.get_all_arguments()
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region = datasource_region.update(params)
        return datasource_region.to_front()

    @BaseHandler.ajax_base()
    def patch(self, datasource_region_id):
        params = self.get_all_arguments()
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region = datasource_region.update(params)
        return datasource_region.to_front()

    @BaseHandler.ajax_base()
    def delete(self, datasource_region_id):
        datasource_region = DatasourceRegion.select(id=datasource_region_id)
        datasource_region.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
