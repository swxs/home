# -*- coding: utf-8 -*-

from const import undefined
from base import BaseHandler
from creater import Creater

class ArticalHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, artical_id=None):
        if artical_id:
            artical = Creater.get_artical_by_artical_id(artical_id)
            return artical.to_front()
        else:
            artical_list = Creater.get_artical_list()
            return artical_list.to_front()

    @BaseHandler.ajax_base
    def post(self):
        title = self.get_argument('title', None)
        author = self.get_argument('author', None)
        source = self.get_argument('source', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        comment_id_list = self.get_arguments('comment_id_list', None)
        artical = Creater.create_artical(title=title, author=author, source=source, summary=summary, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list)
        return artical.to_front()
    
    @BaseHandler.ajax_base
    def put(self, artical_id):
        title = self.get_argument('title', None)
        author = self.get_argument('author', None)
        source = self.get_argument('source', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        comment_id_list = self.get_arguments('comment_id_list', None)
        artical = Creater.get_artical_by_artical_id(artical_id)
        artical.update_artical(title=title, author=author, source=source, summary=summary, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list)
        return artical.to_front()

    @BaseHandler.ajax_base
    def patch(self, artical_id):
        title = self.get_argument('title', undefined)
        author = self.get_argument('author', undefined)
        source = self.get_argument('source', undefined)
        summary = self.get_argument('summary', undefined)
        content = self.get_argument('content', undefined)
        tag_id_list = self.get_arguments('tag_id_list', undefined)
        comment_id_list = self.get_arguments('comment_id_list', undefined)
        artical = Creater.get_artical_by_artical_id(artical_id)
        artical.update_artical(title=title, author=author, source=source, summary=summary, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list)
        return artical.to_front()

    @BaseHandler.ajax_base
    def delete(self, artical_id):
        artical = Creater.get_artical_by_artical_id(artical_id)
        artical.delete_artical()
        return None
