# -*- coding: utf-8 -*-

from const import undefined, TAG_LIST_PER_PAGE
from common.Utils.pagenate import Page
from base import BaseHandler
from . import utils

class TagHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, tag_id=None):
        if tag_id:
            tag = utils.get_tag_by_tag_id(tag_id)
            return utils.to_front(tag)
        else:
            page = self.get_argument('page', 1)
            tag_list = utils.get_tag_list()
            paged_tag_list = Page(
                tag_list,
                page=page,
                items_per_page=TAG_LIST_PER_PAGE)
            return [utils.to_front(tag) for tag in paged_tag_list]

    @BaseHandler.ajax_base
    def post(self):
        name = self.get_argument('name', None)
        color = self.get_argument('color', None)
        length = self.get_argument('length', None)
        tag = utils.create_tag(name=name, color=color, length=length)
        return utils.to_front(tag)
    
    @BaseHandler.ajax_base
    def put(self, tag_id):
        name = self.get_argument('name', None)
        color = self.get_argument('color', None)
        length = self.get_argument('length', None)
        tag = utils.get_tag_by_tag_id(tag_id)
        utils.update_tag(tag, name=name, color=color, length=length)
        return utils.to_front(tag)

    @BaseHandler.ajax_base
    def patch(self, tag_id):
        name = self.get_argument('name', undefined)
        color = self.get_argument('color', undefined)
        length = self.get_argument('length', undefined)
        tag = utils.get_tag_by_tag_id(tag_id)
        utils.update_tag(tag, name=name, color=color, length=length)
        return utils.to_front(tag)

    @BaseHandler.ajax_base
    def delete(self, tag_id):
        tag = utils.get_tag_by_tag_id(tag_id)
        utils.delete_tag(tag)
        return None
