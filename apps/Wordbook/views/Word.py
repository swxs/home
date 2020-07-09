# -*- coding: utf-8 -*-
# @File    : Word.py
# @AUTH    : model

import json
from tornado.web import url
from web.web import BaseHandler
from web.consts import undefined
from web.result import SuccessData
from web.decorator.render import render
from common.Helpers.Helper_pagenate import Page
from common.Utils.log_utils import getLogger
from ..utils.Word import Word, word_schema

log = getLogger("views/word")


class WordHandler(BaseHandler):
    @render
    async def get(self, word_id=None):
        if word_id:
            word = await Word.select(id=word_id)
            return SuccessData(
                data=await word.to_front()
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
            return SuccessData(
                data=pager.items, 
                info=pager.info
            )


    @render
    async def post(self, word_id=None):
        if word_id:
            params = word_schema.load(self.arguments, partial=True)
            old_word = await Word.select(id=word_id)
            new_word = await word.copy(**params.data)
            return SuccessData(
                id=new_word.id
            )
        else:
            params = word_schema.load(self.arguments)
            word = await Word.create(**params.data)
            return SuccessData(
                id=word.id
            )

    @render
    async def put(self, word_id=None):
        params = word_schema.load(self.arguments)
        word = await Word.find_and_update(id=word_id, **params.data)
        return SuccessData(
            id=word.id
        )

    @render
    async def patch(self, word_id=None):
        params = word_schema.load(self.arguments, partial=True)
        word = await Word.find_and_update(id=word_id, **params.data)
        return SuccessData(
            id=word.id
        )

    @render
    async def delete(self, word_id=None):
        count = await Word.find_and_delete(id=word_id)
        return SuccessData(
            count=count
        )

    def set_default_headers(self):
        self._headers.add("version", "1")


URL_MAPPING_LIST = [
    url(r"/api/wordbook/word/(?:([a-zA-Z0-9&%\.~-]+)/)?", WordHandler),
]
