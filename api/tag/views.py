# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
from creater import Creater


class TagHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, tag_id=None):
        ''''''
        if tag_id:
            tag = Creater.get_tag_by_tag_id(tag_id)
            return tag.to_front()
        else:
            tag_list = Creater.get_tag_list()
            return tag_list.to_front()

    @BaseHandler.ajax_base
    def post(self):
        name = self.get_argument('name', None)
        color = self.get_argument('color', None)
        length = self.get_argument('length', None)
        tag = Creater.create_tag(name=name, color=color, length=length)
        return tag.to_front()

    @BaseHandler.ajax_base
    def put(self, tag_id):
        name = self.get_argument('name', None)
        color = self.get_argument('color', None)
        length = self.get_argument('length', None)
        tag = Creater.get_tag_by_tag_id(tag_id)
        tag.update_tag(name=name, color=color, length=length)
        return tag.to_front()

    @BaseHandler.ajax_base
    def patch(self, tag_id):
        name = self.get_argument('name', undefined)
        color = self.get_argument('color', undefined)
        length = self.get_argument('length', undefined)
        tag = Creater.get_tag_by_tag_id(tag_id)
        tag.update_tag(name=name, color=color, length=length)
        return tag.to_front()

    @BaseHandler.ajax_base
    def delete(self, tag_id):
        tag = Creater.get_tag_by_tag_id(tag_id)
        tag.delete_tag()
        return None
