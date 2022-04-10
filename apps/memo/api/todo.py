# -*- coding: utf-8 -*-
# @File    : api/todo.py
# @AUTH    : code_creater

import logging

from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.dependencies.pagination import get_pagination

# 本模块方法
from ..dao.todo import Todo
from ..schemas.todo import TodoSchema

router = APIRouter()

logger = logging.getLogger("main.apps.todo.api.todo")


@router.get("/{todo_id}")
async def get_todo(
    todo_id: str = Path(...),
):
    todo = await Todo.find(
        finds=todo_id,
    )
    return {
        "data": await todo.to_front(),
    }


@router.get("/")
async def get_todo_list(
    todo_schema=Query(...),
    pagination=Depends(get_pagination),
):
    todo_list = await Todo.search(
        searches=todo_schema.dict(exclude_unset=True),
        skip=pagination.skip,
        limit=pagination.limit,
    )
    return {
        "data": await todo_list.to_front(),
        "pagination": await todo_list.get_pagination(),
    }


@router.post("/")
async def create_todo(
    todo_schema: TodoSchema = Body(...),
):
    todo = await Todo.create(
        params=todo_schema.dict(),
    )
    return {
        "data": await todo.to_front(),
    }


@router.post("/{todo_id}")
async def copy_todo(
    todo_id: str = Path(...),
    todo_schema: TodoSchema = Body(...),
):
    todo = await Todo.copy(
        finds=todo_id,
        params=todo_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await todo.to_front(),
    }


@router.put("/{todo_id}")
async def change_todo(
    todo_id: str = Path(...),
    todo_schema: TodoSchema = Body(...),
):
    todo = await Todo.update(
        find=todo_id,
        params=todo_schema.dict(),
    )
    return {
        "data": await todo.to_front(),
    }


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: str = Path(...),
):
    count = await Todo.delete(
        find=todo_id,
    )
    return {
        "count": count,
    }


@router.patch("/{todo_id}")
async def modify_todo(
    todo_id: str = Path(...),
    todo_schema: TodoSchema = Body(...),
):
    todo = await Todo.update(
        find=todo_id,
        params=todo_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await todo.to_front(),
    }
