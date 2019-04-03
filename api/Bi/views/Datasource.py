# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Datasource import Datasource
from common.Utils.log_utils import getLogger

log = getLogger("views/Datasource")


class DatasourceHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_id=None):
        if datasource_id:
            datasource = Datasource.select(id=datasource_id)
            return Datasource.to_front()
        else:
            datasource_list = Datasource.filter()
            return [datasource.to_front() for datasource in datasource_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        datasource = Datasource.create(params)
        return datasource.to_front()

    @BaseHandler.ajax_base()
    def put(self, datasource_id):
        params = self.get_all_arguments()
        datasource = Datasource.select(id=datasource_id)
        datasource = datasource.update(params)
        return datasource.to_front()

    @BaseHandler.ajax_base()
    def patch(self, datasource_id):
        params = self.get_all_arguments()
        datasource = Datasource.select(id=datasource_id)
        datasource = datasource.update(params)
        return datasource.to_front()

    @BaseHandler.ajax_base()
    def delete(self, datasource_id):
        datasource = Datasource.select(id=datasource_id)
        datasource.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
