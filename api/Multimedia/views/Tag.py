# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Tag import Tag
from common.Utils.log_utils import getLogger

log = getLogger("views/Tag")


class TagHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, tag_id=None):
        if tag_id:
            tag = Tag.select(id=tag_id)
            return Tag.to_front()
        else:
            tag_list = Tag.filter()
            return [tag.to_front() for tag in tag_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        tag = Tag.create(params)
        return tag.to_front()

    @BaseHandler.ajax_base()
    def put(self, tag_id):
        params = self.get_all_arguments()
        tag = Tag.select(id=tag_id)
        tag = tag.update(params)
        return tag.to_front()

    @BaseHandler.ajax_base()
    def patch(self, tag_id):
        params = self.get_all_arguments()
        tag = Tag.select(id=tag_id)
        tag = tag.update(params)
        return tag.to_front()

    @BaseHandler.ajax_base()
    def delete(self, tag_id):
        tag = Tag.select(id=tag_id)
        tag.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
