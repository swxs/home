# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Artical import Artical
from common.Utils.log_utils import getLogger

log = getLogger("views/Artical")


class ArticalHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, artical_id=None):
        if artical_id:
            artical = Artical.select(id=artical_id)
            return Artical.to_front()
        else:
            artical_list = Artical.filter()
            return [artical.to_front() for artical in artical_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        artical = Artical.create(params)
        return artical.to_front()

    @BaseHandler.ajax_base()
    def put(self, artical_id):
        params = self.get_all_arguments()
        artical = Artical.select(id=artical_id)
        artical = artical.update(params)
        return artical.to_front()

    @BaseHandler.ajax_base()
    def patch(self, artical_id):
        params = self.get_all_arguments()
        artical = Artical.select(id=artical_id)
        artical = artical.update(params)
        return artical.to_front()

    @BaseHandler.ajax_base()
    def delete(self, artical_id):
        artical = Artical.select(id=artical_id)
        artical.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
