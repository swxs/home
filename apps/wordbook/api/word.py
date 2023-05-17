# -*- coding: utf-8 -*-
# @File    : api/word.py
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
from ..dao.word import Word
from ..schemas.word import WordSchema, get_word_schema

router = APIRouter()

logger = logging.getLogger("main.apps.wordbook.api.word")


@router.get("/")
async def get_word_list(
    token_schema: TokenSchema = Depends(get_token),
    word_schema: WordSchema = Depends(get_word_schema),
    page_schema: PageSchema = Depends(get_pagination),
):
    word_list = (
        await Word.search(
            searches=word_schema.dict(exclude_unset=True),
            skip=page_schema.skip,
            limit=page_schema.limit,
        )
    ).order_by(page_schema.order_by)

    pagination = PaginationSchema(
        total=await Word.count(
            finds=word_schema.dict(exclude_unset=True),
        ),
        order_by=page_schema.order_by,
        use_pager=page_schema.use_pager,
        page=page_schema.page,
        page_number=page_schema.page_number,
    )

    return success(
        {
            "data": await word_list.to_dict(),
            "pagination": pagination.dict(),
        }
    )


@router.get("/{word_id}")
async def get_word(
    token_schema: TokenSchema = Depends(get_token),
    word_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    word = await Word.find_one(
        finds={"id": ObjectId(word_id)},
    )

    return success(
        {
            "data": word,
        }
    )


@router.post("/")
async def create_word(
    token_schema: TokenSchema = Depends(get_token),
    word_schema: WordSchema = Body(...),
):
    word = await Word.create(
        params=word_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": word,
        }
    )


@router.put("/{word_id}")
async def modify_word(
    token_schema: TokenSchema = Depends(get_token),
    word_id: OID = Path(..., regex="[0-9a-f]{24}"),
    word_schema: WordSchema = Body(...),
):
    word = await Word.update_one(
        finds={"id": ObjectId(word_id)},
        params=word_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": word,
        }
    )


@router.delete("/{word_id}")
async def delete_word(
    token_schema: TokenSchema = Depends(get_token),
    word_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    count = await Word.delete_one(
        finds={"id": ObjectId(word_id)},
    )

    return success(
        {
            "count": count,
        }
    )
