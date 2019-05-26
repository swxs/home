# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Datasource import Datasource

log = getLogger("views/Datasource")


class DatasourceHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datasource_id=None):
        if datasource_id:
            datasource = Datasource.select(id=datasource_id)
            return datasource.to_front()
        else:
            datasource_list = Datasource.filter()
            return [datasource.to_front() for datasource in datasource_list]

    @BaseHandler.ajax_base()
    def post(self, datasource_id=None):
        if datasource_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            datasource = Datasource.select(id=datasource_id)
            datasource = datasource.copy(**params)
            return datasource.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            datasource = Datasource.create(**params)
            return datasource.id

    @BaseHandler.ajax_base()
    def put(self, datasource_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        datasource = Datasource.select(id=datasource_id)
        datasource = datasource.update(**params)
        return datasource.id

    @BaseHandler.ajax_base()
    def patch(self, datasource_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        datasource = Datasource.select(id=datasource_id)
        datasource = datasource.update(**params)
        return datasource.id

    @BaseHandler.ajax_base()
    def delete(self, datasource_id=None):
        datasource = Datasource.select(id=datasource_id)
        datasource.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
