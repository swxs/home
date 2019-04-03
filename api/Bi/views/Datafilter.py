# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Datafilter import Datafilter
from common.Utils.log_utils import getLogger

log = getLogger("views/Datafilter")


class DatafilterHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datafilter_id=None):
        if datafilter_id:
            datafilter = Datafilter.select(id=datafilter_id)
            return Datafilter.to_front()
        else:
            datafilter_list = Datafilter.filter()
            return [datafilter.to_front() for datafilter in datafilter_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        datafilter = Datafilter.create(params)
        return datafilter.to_front()

    @BaseHandler.ajax_base()
    def put(self, datafilter_id):
        params = self.get_all_arguments()
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter = datafilter.update(params)
        return datafilter.to_front()

    @BaseHandler.ajax_base()
    def patch(self, datafilter_id):
        params = self.get_all_arguments()
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter = datafilter.update(params)
        return datafilter.to_front()

    @BaseHandler.ajax_base()
    def delete(self, datafilter_id):
        datafilter = Datafilter.select(id=datafilter_id)
        datafilter.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
