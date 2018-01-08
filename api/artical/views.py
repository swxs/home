# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
import enums as enums
import utils as utils

class ArticalHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, artical_id=None):
        ''''''
        if artical_id:
            artical = utils.get_artical_by_artical_id(artical_id)
            return utils.to_front(artical)
        else:
            artical_list = utils.get_artical_list()
            return [utils.to_front(artical) for artical in artical_list]


    @BaseHandler.ajax_base
    def post(self):
        title = self.get_argument('title', None)
        author = self.get_argument('author', None)
        source = self.get_argument('source', None)
        content = self.get_argument('content', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        comment_id_list = self.get_arguments('comment_id_list', None)
        summary = self.get_argument('summary', None)
        artical = utils.create(title=title, author=author, source=source, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list, summary=summary)
        return utils.to_front(artical)
    
    @BaseHandler.ajax_base
    def put(self, artical_id):
        title = self.get_argument('title', None)
        author = self.get_argument('author', None)
        source = self.get_argument('source', None)
        content = self.get_argument('content', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        comment_id_list = self.get_arguments('comment_id_list', None)
        summary = self.get_argument('summary', None)
        artical = utils.get_artical_by_artical_id(artical_id)
        artical = utils.update(artical, title=title, author=author, source=source, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list, summary=summary)
        return utils.to_front(artical)
    
    @BaseHandler.ajax_base
    def patch(self, artical_id):
        title = self.get_argument('title', undefined)
        author = self.get_argument('author', undefined)
        source = self.get_argument('source', undefined)
        content = self.get_argument('content', undefined)
        tag_id_list = self.get_arguments('tag_id_list', undefined)
        comment_id_list = self.get_arguments('comment_id_list', undefined)
        summary = self.get_argument('summary', undefined)
        artical = utils.get_artical_by_artical_id(artical_id)
        artical = utils.update(artical, title=title, author=author, source=source, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list, summary=summary)
        return utils.to_front(artical)
            
    @BaseHandler.ajax_base
    def delete(self, artical_id):
        artical = utils.get_artical_by_artical_id(artical_id)
        utils.delete(artical)
        return None
