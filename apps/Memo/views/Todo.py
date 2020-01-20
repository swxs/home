# -*- coding: utf-8 -*-
# @File    : Todo.py
# @AUTH    : model

import json
from document_utils.consts import undefined
from common.Decorator.render import render
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from result import SuccessData
from ...BaseConsts import *
from ...BaseViews import BaseHandler
from ..utils.Todo import Todo, TodoSchema

log = getLogger("views/todo")


class TodoHandler(BaseHandler):
    @render
    async def get(self, todo_id=None):
        if todo_id:
            todo = await Todo.select(id=todo_id)
            return SuccessData(
                await todo.to_front()
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
            return SuccessData(pager.items, info=pager.info)


    @render
    async def post(self, todo_id=None):
        if todo_id:
            params = TodoSchema.load(self.arguments, partial=True)
            todo = await Todo.select(id=todo_id)
            todo = await todo.copy(**params)
            return SuccessData(
                id=todo.id
            )
        else:
            params = TodoSchema.load(self.arguments)
            todo = await Todo.create(**params)
            return SuccessData(
                id=todo.id
            )

    @render
    async def put(self, todo_id=None):
        params = TodoSchema.load(self.arguments)
        todo = await Todo.find_and_update(id=todo_id, **params)
        return SuccessData(
            id=todo.id
        )

    @render
    async def patch(self, todo_id=None):
        params = TodoSchema.load(self.arguments, partial=True)
        todo = await Todo.find_and_update(id=todo_id, **params)
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
