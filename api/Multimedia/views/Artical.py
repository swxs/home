# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Artical import Artical

log = getLogger("views/Artical")


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
    def post(self, artical_id=None):
        if artical_id:
            params = dict()
            params['title'] = self.get_argument('title', undefined)
            params['author'] = self.get_argument('author', undefined)
            params['year'] = self.get_argument('year', undefined)
            params['source'] = self.get_argument('source', undefined)
            params['summary'] = self.get_argument('summary', undefined)
            params['content'] = self.get_argument('content', undefined)
            params['ttype_id_list'] = self.get_argument('ttype_id_list', undefined)
            params['tag_id_list'] = self.get_argument('tag_id_list', undefined)
            params['comment_id_list'] = self.get_argument('comment_id_list', undefined)
            artical = Artical.select(id=artical_id)
            artical = artical.copy(**params)
            return artical.id
        else:
            params = dict()
            params['title'] = self.get_argument('title', None)
            params['author'] = self.get_argument('author', None)
            params['year'] = self.get_argument('year', None)
            params['source'] = self.get_argument('source', None)
            params['summary'] = self.get_argument('summary', None)
            params['content'] = self.get_argument('content', None)
            params['ttype_id_list'] = self.get_argument('ttype_id_list', None)
            params['tag_id_list'] = self.get_argument('tag_id_list', None)
            params['comment_id_list'] = self.get_argument('comment_id_list', None)
            artical = Artical.create(**params)
            return artical.id

    @BaseHandler.ajax_base()
    def put(self, artical_id=None):
        params = dict()
        params['title'] = self.get_argument('title', None)
        params['author'] = self.get_argument('author', None)
        params['year'] = self.get_argument('year', None)
        params['source'] = self.get_argument('source', None)
        params['summary'] = self.get_argument('summary', None)
        params['content'] = self.get_argument('content', None)
        params['ttype_id_list'] = self.get_argument('ttype_id_list', None)
        params['tag_id_list'] = self.get_argument('tag_id_list', None)
        params['comment_id_list'] = self.get_argument('comment_id_list', None)
        artical = Artical.select(id=artical_id)
        artical = artical.update(**params)
        return artical.id

    @BaseHandler.ajax_base()
    def patch(self, artical_id=None):
        params = dict()
        params['title'] = self.get_argument('title', undefined)
        params['author'] = self.get_argument('author', undefined)
        params['year'] = self.get_argument('year', undefined)
        params['source'] = self.get_argument('source', undefined)
        params['summary'] = self.get_argument('summary', undefined)
        params['content'] = self.get_argument('content', undefined)
        params['ttype_id_list'] = self.get_argument('ttype_id_list', undefined)
        params['tag_id_list'] = self.get_argument('tag_id_list', undefined)
        params['comment_id_list'] = self.get_argument('comment_id_list', undefined)
        artical = Artical.select(id=artical_id)
        artical = artical.update(**params)
        return artical.id

    @BaseHandler.ajax_base()
    def delete(self, artical_id=None):
        artical = Artical.select(id=artical_id)
        artical.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")
