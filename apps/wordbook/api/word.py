# -*- coding: utf-8 -*-
# @File    : api/word.py
# @AUTH    : code_creater

import logging

from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.dependencies.pagination import get_pagination

# 本模块方法
from ..dao.word import Word
from ..schemas.word import WordSchema

router = APIRouter()

logger = logging.getLogger("main.apps.word.api.word")


@router.get("/{word_id}")
async def get_word(
    word_id: str = Path(...),
):
    word = await Word.find(
        finds=word_id,
    )
    return {
        "data": await word.to_front(),
    }


@router.get("/")
async def get_word_list(
    word_schema=Query(...),
    pagination=Depends(get_pagination),
):
    word_list = await Word.search(
        searches=word_schema.dict(exclude_unset=True),
        skip=pagination.skip,
        limit=pagination.limit,
    )
    return {
        "data": await word_list.to_front(),
        "pagination": await word_list.get_pagination(),
    }


@router.post("/")
async def create_word(
    word_schema: WordSchema = Body(...),
):
    word = await Word.create(
        params=word_schema.dict(),
    )
    return {
        "data": await word.to_front(),
    }


@router.post("/{word_id}")
async def copy_word(
    word_id: str = Path(...),
    word_schema: WordSchema = Body(...),
):
    word = await Word.copy(
        finds=word_id,
        params=word_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await word.to_front(),
    }


@router.put("/{word_id}")
async def change_word(
    word_id: str = Path(...),
    word_schema: WordSchema = Body(...),
):
    word = await Word.update(
        find=word_id,
        params=word_schema.dict(),
    )
    return {
        "data": await word.to_front(),
    }


@router.delete("/{word_id}")
async def delete_word(
    word_id: str = Path(...),
):
    count = await Word.delete(
        find=word_id,
    )
    return {
        "count": count,
    }


@router.patch("/{word_id}")
async def modify_word(
    word_id: str = Path(...),
    word_schema: WordSchema = Body(...),
):
    word = await Word.update(
        find=word_id,
        params=word_schema.dict(exclude_defaults=True),
    )
    return {
        "data": await word.to_front(),
    }
