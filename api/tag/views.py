# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
import enums as enums
import utils as utils

class TagHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, tag_id=None):
        ''''''
        if tag_id:
            tag = utils.get_tag_by_tag_id(tag_id)
            return utils.to_front(tag)
        else:
            tag_list = utils.get_tag_list()
            return [utils.to_front(tag) for tag in tag_list]


    @BaseHandler.ajax_base
    def post(self):
        
        name = self.get_argument('name', None)
        color = self.get_argument('color', None)
        length = self.get_argument('length', None)
        tag = utils.create(name=name, color=color, length=length)
        return utils.to_front(tag)
    
    @BaseHandler.ajax_base
    def put(self, tag_id):
        
        name = self.get_argument('name', None)
        color = self.get_argument('color', None)
        length = self.get_argument('length', None)
        tag = utils.get_tag_by_tag_id(tag_id)
        tag = utils.update(tag, name=name, color=color, length=length)
        return utils.to_front(tag)
    
    @BaseHandler.ajax_base
    def patch(self, tag_id):
        
        name = self.get_argument('name', undefined)
        color = self.get_argument('color', undefined)
        length = self.get_argument('length', undefined)
        tag = utils.get_tag_by_tag_id(tag_id)
        tag = utils.update(tag, name=name, color=color, length=length)
        return utils.to_front(tag)
            
    @BaseHandler.ajax_base
    def delete(self, tag_id):
        tag = utils.get_tag_by_tag_id(tag_id)
        utils.delete(tag)
        return None
