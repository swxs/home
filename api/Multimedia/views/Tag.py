# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Tag import Tag

log = getLogger("views/Tag")


class TagHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, tag_id=None):
        if tag_id:
            tag = Tag.select(id=tag_id)
            return tag.to_front()
        else:
            tag_list = Tag.filter()
            return [tag.to_front() for tag in tag_list]

    @BaseHandler.ajax_base()
    def post(self, tag_id=None):
        if tag_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['color'] = self.get_argument('color', undefined)
            tag = Tag.select(id=tag_id)
            tag = tag.copy(**params)
            return tag.id
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['color'] = self.get_argument('color', None)
            tag = Tag.create(**params)
            return tag.id

    @BaseHandler.ajax_base()
    def put(self, tag_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['color'] = self.get_argument('color', None)
        tag = Tag.select(id=tag_id)
        tag = tag.update(**params)
        return tag.id

    @BaseHandler.ajax_base()
    def patch(self, tag_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['color'] = self.get_argument('color', undefined)
        tag = Tag.select(id=tag_id)
        tag = tag.update(**params)
        return tag.id

    @BaseHandler.ajax_base()
    def delete(self, tag_id=None):
        tag = Tag.select(id=tag_id)
        tag.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
