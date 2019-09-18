# -*- coding: utf-8 -*-
# @File    : Artical.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Artical import Artical

log = getLogger("views/Artical")


class ArticalHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, artical_id=None):
        if artical_id:
            artical = Artical.select(id=artical_id)
            return SuccessData(
                artical.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            artical_cursor = Artical.search(**search_params)
            data = []
            for artical in artical_cursor:
                data.append(artical.to_front())
            return SuccessData(data)
            # pager = Page(artical_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

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
            return SuccessData(
                artical.id
            )
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
            return SuccessData(
                artical.id
            )

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
        return SuccessData(
            artical.id
        )

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
        return SuccessData(
            artical.id
        )

    @BaseHandler.ajax_base()
    def delete(self, artical_id=None):
        artical = Artical.select(id=artical_id)
        artical.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
