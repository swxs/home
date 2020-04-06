# -*- coding: utf-8 -*-
# @File    : Todo.py
# @AUTH    : model

import json
from tornado.web import url
from web.web import BaseHandler
from web.consts import undefined
from web.result import SuccessData
from web.decorator.render import render
from common.Helpers.Helper_pagenate import Page
from common.Utils.log_utils import getLogger
from ..utils.Todo import Todo, todo_schema

log = getLogger("views/todo")


class TodoHandler(BaseHandler):
    @render
    async def get(self, todo_id=None):
        if todo_id:
            todo = await Todo.select(id=todo_id)
            return SuccessData(
                data=await todo.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            order_by = self.get_argument("order_by", "")
            use_pager = int(self.get_argument("use_pager", 1))
            page = int(self.get_argument("page", 1))
            items_per_page = int(self.get_argument("items_per_page", 20))

            item_count = await Todo.count(**search_params)
            if use_pager:
                search_params.update({
                    "limit": items_per_page,
                    "skip": (page - 1) * items_per_page
                })
            order_by = [o for o in order_by.split(";") if bool(o)]
            todo_cursor = Todo.search(**search_params).order_by(order_by)
            data = [await  todo.to_front() async for todo in todo_cursor]
            pager = Page(data, use_pager=use_pager, page=page, items_per_page=items_per_page, item_count=item_count)
            return SuccessData(
                data=pager.items, 
                info=pager.info
            )


    @render
    async def post(self, todo_id=None):
        if todo_id:
            params = todo_schema.load(self.arguments, partial=True)
            old_todo = await Todo.select(id=todo_id)
            new_todo = await old_todo.copy(**params.data)
            return SuccessData(
                id=new_todo.id
            )
        else:
            params = todo_schema.load(self.arguments)
            todo = await Todo.create(**params.data)
            return SuccessData(
                id=todo.id
            )

    @render
    async def put(self, todo_id=None):
        params = todo_schema.load(self.arguments)
        todo = await Todo.find_and_update(id=todo_id, **params.data)
        return SuccessData(
            id=todo.id
        )

    @render
    async def patch(self, todo_id=None):
        params = todo_schema.load(self.arguments, partial=True)
        todo = await Todo.find_and_update(id=todo_id, **params.data)
        return SuccessData(
            id=todo.id
        )

    @render
    async def delete(self, todo_id=None):
        count = await Todo.find_and_delete(id=todo_id)
        return SuccessData(
            count=count
        )

    def set_default_headers(self):
        self._headers.add("version", "1")


URL_MAPPING_LIST = [
    url(r"/api/memo/todo/(?:([a-zA-Z0-9&%\.~-]+)/)?", TodoHandler),
]
