# -*- coding: utf-8 -*-

from base import BaseHandler
from api.consts.const import undefined
from api.utils.artical import Artical


class ArticalHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, artical_id=None):
        if artical_id:
            artical = Artical.select(id=artical_id)
            return artical.to_front()
        else:
            artical_list = Artical.filter()
            return [artical.to_front() for artical in artical_list]

    @BaseHandler.ajax_base()
    def post(self):
        title = self.get_argument('title', None)
        author = self.get_argument('author', None)
        source = self.get_argument('source', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        comment_id_list = self.get_arguments('comment_id_list', None)
        artical = Artical.create(
            title=title,
            author=author,
            source=source,
            summary=summary,
            content=content,
            tag_id_list=tag_id_list,
            comment_id_list=comment_id_list
        )
        return artical.to_front()

    @BaseHandler.ajax_base()
    def put(self, artical_id):
        title = self.get_argument('title', None)
        author = self.get_argument('author', None)
        source = self.get_argument('source', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        tag_id_list = self.get_arguments('tag_id_list', None)
        comment_id_list = self.get_arguments('comment_id_list', None)
        artical = Artical.select(id=artical_id)
        artical = artical.update(
            title=title,
            author=author,
            source=source,
            summary=summary,
            content=content,
            tag_id_list=tag_id_list,
            comment_id_list=comment_id_list
        )
        return artical.to_front()

    @BaseHandler.ajax_base()
    def patch(self, artical_id):
        title = self.get_argument('title', undefined)
        author = self.get_argument('author', undefined)
        source = self.get_argument('source', undefined)
        summary = self.get_argument('summary', undefined)
        content = self.get_argument('content', undefined)
        tag_id_list = self.get_arguments('tag_id_list', undefined)
        comment_id_list = self.get_arguments('comment_id_list', undefined)
        artical = Artical.select(id=artical_id)
        artical = artical.update(
            title=title,
            author=author,
            source=source,
            summary=summary,
            content=content,
            tag_id_list=tag_id_list,
            comment_id_list=comment_id_list
        )
        return artical.to_front()

    @BaseHandler.ajax_base()
    def delete(self, artical_id):
        artical = Artical.select(id=artical_id)
        artical.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
