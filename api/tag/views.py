# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
import enum as enum
from creater import creater


class TagHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, tag_id=None):
        ''''''
        if tag_id:
            tag = creater.get_tag_by_tag_id(tag_id)
        else:
            tag = creater.get_tag_list()
        return tag.to_front()

    @BaseHandler.ajax_base
    def post(self):
        ''''''
        name = self.get_argument('name', None)
        ttype = self.get_argument('ttype', None)
        tag = creater.create(name=name, ttype=ttype)
        return tag.to_front()

    @BaseHandler.ajax_base
    def put(self, tag_id):
        name = self.get_argument('name', None)
        ttype = self.get_argument('ttype', None)
        tag = creater.get_tag_by_tag_id(tag_id)
        tag.update(name=name, ttype=ttype)
        return tag.to_front()

    @BaseHandler.ajax_base
    def patch(self, tag_id):
        name = self.get_argument('name', undefined)
        ttype = self.get_argument('ttype', undefined)
        tag = creater.get_tag_by_tag_id(tag_id)
        tag.update(name=name, ttype=ttype)
        return tag.to_front()

    @BaseHandler.ajax_base
    def delete(self, tag_id):
        tag = creater.get_tag_by_tag_id(tag_id)
        tag.delete()
        return None
