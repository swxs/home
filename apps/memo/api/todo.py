# -*- coding: utf-8 -*-
# @File    : api/todo.py
# @AUTH    : code_creater

import logging

from bson import ObjectId
from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.response import success
from web.custom_types import OID
from web.dependencies.token import TokenSchema, get_token
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination

# 本模块方法
from ..dao.todo import Todo
from ..schemas.todo import TodoSchema, get_todo_schema

router = APIRouter()

logger = logging.getLogger("main.apps.todo.api.todo")


@router.get("/")
async def get_todo_list(
    token_schema: TokenSchema = Depends(get_token),
    todo_schema: TodoSchema = Depends(get_todo_schema),
    page_schema: PageSchema = Depends(get_pagination),
):
    todo_list = (
        await Todo.search(
            searches=todo_schema.dict(exclude_unset=True),
            skip=page_schema.skip,
            limit=page_schema.limit,
        )
    ).order_by(page_schema.order_by)

    pagination = PaginationSchema(
        total=await Todo.count(
            finds=todo_schema.dict(exclude_unset=True),
        ),
        order_by=page_schema.order_by,
        use_pager=page_schema.use_pager,
        page=page_schema.page,
        page_number=page_schema.page_number,
    )

    return success(
        {
            "data": await todo_list.to_dict(),
            "pagination": pagination.dict(),
        }
    )


@router.get("/{todo_id}")
async def get_todo(
    token_schema: TokenSchema = Depends(get_token),
    todo_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    todo = await Todo.find_one(
        finds={"id": ObjectId(todo_id)},
    )

    return success(
        {
            "data": todo,
        }
    )


@router.post("/")
async def create_todo(
    token_schema: TokenSchema = Depends(get_token),
    todo_schema: TodoSchema = Body(...),
):
    todo = await Todo.create(
        params=todo_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": todo,
        }
    )


@router.put("/{todo_id}")
async def modify_todo(
    token_schema: TokenSchema = Depends(get_token),
    todo_id: OID = Path(..., regex="[0-9a-f]{24}"),
    todo_schema: TodoSchema = Body(...),
):
    todo = await Todo.update_one(
        finds={"id": ObjectId(todo_id)},
        params=todo_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": todo,
        }
    )


@router.delete("/{todo_id}")
async def delete_todo(
    token_schema: TokenSchema = Depends(get_token),
    todo_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    count = await Todo.delete_one(
        finds={"id": ObjectId(todo_id)},
    )

    return success(
        {
            "count": count,
        }
    )
