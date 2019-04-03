# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Ttype import Ttype
from common.Utils.log_utils import getLogger

log = getLogger("views/Ttype")


class TtypeHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, ttype_id=None):
        if ttype_id:
            ttype = Ttype.select(id=ttype_id)
            return Ttype.to_front()
        else:
            ttype_list = Ttype.filter()
            return [ttype.to_front() for ttype in ttype_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        ttype = Ttype.create(params)
        return ttype.to_front()

    @BaseHandler.ajax_base()
    def put(self, ttype_id):
        params = self.get_all_arguments()
        ttype = Ttype.select(id=ttype_id)
        ttype = ttype.update(params)
        return ttype.to_front()

    @BaseHandler.ajax_base()
    def patch(self, ttype_id):
        params = self.get_all_arguments()
        ttype = Ttype.select(id=ttype_id)
        ttype = ttype.update(params)
        return ttype.to_front()

    @BaseHandler.ajax_base()
    def delete(self, ttype_id):
        ttype = Ttype.select(id=ttype_id)
        ttype.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
