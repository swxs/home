# -*- coding: utf-8 -*-

from const import undefined, ARTICAL_LIST_PER_PAGE
from common.Utils.pagenate import Page
from base import BaseHandler
import utils

class ArticalHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self, artical_id=None):
        if artical_id:
            artical = utils.get_artical_by_artical_id(artical_id)
            return artical.to_front()
        else:
            page = self.get_argument('page', 1)
            artical_list = utils.get_artical_list()
            paged_artical_list = Page(
                artical_list,
                page=page,
                items_per_page=ARTICAL_LIST_PER_PAGE)
            return [utils.to_front(artical) for artical in paged_artical_list]

    @BaseHandler.ajax_base
    def post(self):
        title = self.get_argument('title', None)
        author = self.get_argument('author', None)
        source = self.get_argument('source', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        comment_id_list = self.get_arguments('comment_id_list', None)
        artical = utils.create_artical(title=title, author=author, source=source, summary=summary, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list)
        return utils.to_front(artical)
    
    @BaseHandler.ajax_base
    def put(self, artical_id):
        title = self.get_argument('title', None)
        author = self.get_argument('author', None)
        source = self.get_argument('source', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        comment_id_list = self.get_arguments('comment_id_list', None)
        artical = utils.get_artical_by_artical_id(artical_id)
        utils.update_artical(artical, title=title, author=author, source=source, summary=summary, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list)
        return utils.to_front(artical)

    @BaseHandler.ajax_base
    def patch(self, artical_id):
        title = self.get_argument('title', undefined)
        author = self.get_argument('author', undefined)
        source = self.get_argument('source', undefined)
        summary = self.get_argument('summary', undefined)
        content = self.get_argument('content', undefined)
        tag_id_list = self.get_arguments('tag_id_list', undefined)
        comment_id_list = self.get_arguments('comment_id_list', undefined)
        artical = utils.get_artical_by_artical_id(artical_id)
        utils.update_artical(artical, title=title, author=author, source=source, summary=summary, content=content, tag_id_list=tag_id_list, comment_id_list=comment_id_list)
        return utils.to_front(artical)

    @BaseHandler.ajax_base
    def delete(self, artical_id):
        artical = utils.get_artical_by_artical_id(artical_id)
        utils.delete_artical(artical)
        return None
