# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Ttype import Ttype

log = getLogger("views/Ttype")


class TtypeHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, ttype_id=None):
        if ttype_id:
            ttype = Ttype.select(id=ttype_id)
            return ttype.to_front()
        else:
            ttype_list = Ttype.filter()
            return [ttype.to_front() for ttype in ttype_list]

    @BaseHandler.ajax_base()
    def post(self, ttype_id=None):
        if ttype_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            ttype = Ttype.select(id=ttype_id)
            ttype = ttype.copy(**params)
            return ttype.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            ttype = Ttype.create(**params)
            return ttype.id

    @BaseHandler.ajax_base()
    def put(self, ttype_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        ttype = Ttype.select(id=ttype_id)
        ttype = ttype.update(**params)
        return ttype.id

    @BaseHandler.ajax_base()
    def patch(self, ttype_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        ttype = Ttype.select(id=ttype_id)
        ttype = ttype.update(**params)
        return ttype.id

    @BaseHandler.ajax_base()
    def delete(self, ttype_id=None):
        ttype = Ttype.select(id=ttype_id)
        ttype.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
