# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Datamerge import Datamerge
from common.Utils.log_utils import getLogger

log = getLogger("views/Datamerge")


class DatamergeHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datamerge_id=None):
        if datamerge_id:
            datamerge = Datamerge.select(id=datamerge_id)
            return Datamerge.to_front()
        else:
            datamerge_list = Datamerge.filter()
            return [datamerge.to_front() for datamerge in datamerge_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        datamerge = Datamerge.create(params)
        return datamerge.to_front()

    @BaseHandler.ajax_base()
    def put(self, datamerge_id):
        params = self.get_all_arguments()
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge = datamerge.update(params)
        return datamerge.to_front()

    @BaseHandler.ajax_base()
    def patch(self, datamerge_id):
        params = self.get_all_arguments()
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge = datamerge.update(params)
        return datamerge.to_front()

    @BaseHandler.ajax_base()
    def delete(self, datamerge_id):
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
