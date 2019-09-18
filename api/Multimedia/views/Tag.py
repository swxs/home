# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Tag import Tag

log = getLogger("views/Tag")


class TagHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, tag_id=None):
        if tag_id:
            tag = Tag.select(id=tag_id)
            return SuccessData(
                tag.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            tag_cursor = Tag.search(**search_params)
            data = []
            for tag in tag_cursor:
                data.append(tag.to_front())
            return SuccessData(data)
            # pager = Page(tag_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    def post(self, tag_id=None):
        if tag_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['color'] = self.get_argument('color', undefined)
            tag = Tag.select(id=tag_id)
            tag = tag.copy(**params)
            return SuccessData(
                tag.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['color'] = self.get_argument('color', None)
            tag = Tag.create(**params)
            return SuccessData(
                tag.id
            )

    @BaseHandler.ajax_base()
    def put(self, tag_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['color'] = self.get_argument('color', None)
        tag = Tag.select(id=tag_id)
        tag = tag.update(**params)
        return SuccessData(
            tag.id
        )

    @BaseHandler.ajax_base()
    def patch(self, tag_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['color'] = self.get_argument('color', undefined)
        tag = Tag.select(id=tag_id)
        tag = tag.update(**params)
        return SuccessData(
            tag.id
        )

    @BaseHandler.ajax_base()
    def delete(self, tag_id=None):
        tag = Tag.select(id=tag_id)
        tag.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
