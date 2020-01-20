# -*- coding: utf-8 -*-
# @File    : Word.py
# @AUTH    : model

import json
from document_utils.consts import undefined
from common.Decorator.render import render
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from result import SuccessData
from ...BaseConsts import *
from ...BaseViews import BaseHandler
from ..utils.Word import Word

log = getLogger("views/word")


class WordHandler(BaseHandler):
    @render
    async def get(self, word_id=None):
        if word_id:
            word = await Word.select(id=word_id)
            return SuccessData(
                await word.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            order_by = self.get_argument("order_by", "")
            use_pager = int(self.get_argument("use_pager", 1))
            page = int(self.get_argument("page", 1))
            items_per_page = int(self.get_argument("items_per_page", 20))

            item_count = await Word.count(**search_params)
            if use_pager:
                search_params.update({
                    "limit": items_per_page,
                    "skip": (page - 1) * items_per_page
                })
            order_by = [o for o in order_by.split(";") if bool(o)]
            word_cursor = Word.search(**search_params).order_by(order_by)
            data = [await  word.to_front() async for word in word_cursor]
            pager = Page(data, use_pager=use_pager, page=page, items_per_page=items_per_page, item_count=item_count)
            return SuccessData(pager.items, info=pager.info)


    @render
    async def post(self, word_id=None):
        if word_id:
            params = dict()
            params['en'] = self.get_argument('en', undefined)
            params['cn'] = self.get_argument('cn', undefined)
            params['number'] = self.get_argument('number', undefined)
            params['last_time'] = self.get_argument('last_time', undefined)
            word = await Word.select(id=word_id)
            word = await word.copy(**params)
            return SuccessData(
                word.id
            )
        else:
            params = dict()
            params['en'] = self.get_argument('en', None)
            params['cn'] = self.get_argument('cn', None)
            params['number'] = self.get_argument('number', None)
            params['last_time'] = self.get_argument('last_time', None)
            word = await Word.create(**params)
            return SuccessData(
                word.id
            )

    @render
    async def put(self, word_id=None):
        params = dict()
        params['en'] = self.get_argument('en', None)
        params['cn'] = self.get_argument('cn', None)
        params['number'] = self.get_argument('number', None)
        params['last_time'] = self.get_argument('last_time', None)
        word = await Word.select(id=word_id)
        word = await word.update(**params)
        return SuccessData(
            word.id
        )

    @render
    async def patch(self, word_id=None):
        params = dict()
        params['en'] = self.get_argument('en', undefined)
        params['cn'] = self.get_argument('cn', undefined)
        params['number'] = self.get_argument('number', undefined)
        params['last_time'] = self.get_argument('last_time', undefined)
        word = await Word.select(id=word_id)
        word = await word.update(**params)
        return SuccessData(
            word.id
        )

    @render
    async def delete(self, word_id=None):
        word = await Word.select(id=word_id)
        await word.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")
