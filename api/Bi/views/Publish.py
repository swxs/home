# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Publish import Publish
from common.Utils.log_utils import getLogger

log = getLogger("views/Publish")


class PublishHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, publish_id=None):
        if publish_id:
            publish = Publish.select(id=publish_id)
            return Publish.to_front()
        else:
            publish_list = Publish.filter()
            return [publish.to_front() for publish in publish_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        publish = Publish.create(params)
        return publish.to_front()

    @BaseHandler.ajax_base()
    def put(self, publish_id):
        params = self.get_all_arguments()
        publish = Publish.select(id=publish_id)
        publish = publish.update(params)
        return publish.to_front()

    @BaseHandler.ajax_base()
    def patch(self, publish_id):
        params = self.get_all_arguments()
        publish = Publish.select(id=publish_id)
        publish = publish.update(params)
        return publish.to_front()

    @BaseHandler.ajax_base()
    def delete(self, publish_id):
        publish = Publish.select(id=publish_id)
        publish.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
