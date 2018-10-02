# -*- coding: utf-8 -*-

from base import BaseHandler
from api.consts.const import undefined
from api.utils.tag import Tag


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
    def post(self):
        name = self.get_argument('name', None)
        color = self.get_argument('color', None)
        length = self.get_argument('length', None)
        tag = Tag.create(name=name, color=color, length=length)
        return tag.to_front()

    @BaseHandler.ajax_base()
    def put(self, tag_id):
        name = self.get_argument('name', None)
        color = self.get_argument('color', None)
        length = self.get_argument('length', None)
        tag = Tag.select(id=tag_id)
        tag = tag.update(name=name, color=color, length=length)
        return tag.to_front()

    @BaseHandler.ajax_base()
    def patch(self, tag_id):
        name = self.get_argument('name', undefined)
        color = self.get_argument('color', undefined)
        length = self.get_argument('length', undefined)
        tag = Tag.select(id=tag_id)
        tag = tag.update(name=name, color=color, length=length)
        return tag.to_front()

    @BaseHandler.ajax_base()
    def delete(self, tag_id):
        tag = Tag.select(id=tag_id)
        tag.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
