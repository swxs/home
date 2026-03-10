# -*- coding: utf-8 -*-
# @File    : api/completion.py
# @AUTH    : code_creater

import logging
import datetime
from typing import Optional

from fastapi import APIRouter, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..models.sudoku_completion import SudokuCompletion
from ..schemas.response import SudokuCompletionSearchResponse
from ..schemas.sudoku_completion import (
    SudokuCompletionCreateSchema,
    SudokuCompletionItemSchema,
)

router = APIRouter()
logger = logging.getLogger("main.apps.sudoku.api.completion")


def _row_to_item(completion, puzzle) -> dict:
    item = SudokuCompletionItemSchema.model_validate(completion).model_dump(mode="json")
    if puzzle is not None:
        item["puzzle_date"] = getattr(puzzle, "puzzle_date", None)
        item["difficulty"] = getattr(puzzle, "difficulty", None)
        if item["difficulty"] is not None and hasattr(item["difficulty"], "value"):
            item["difficulty"] = item["difficulty"].value
    return item


@router.get("/me", response_model=SuccessResponse[SudokuCompletionSearchResponse])
async def get_my_completions(
    token_schema: TokenSchema = Depends(get_token),
    page_schema: PageSchema = Depends(get_pagination),
    puzzle_id: Optional[str] = Query(None, description="谜题ID"),
    puzzle_date_from: Optional[str] = Query(None, description="谜题日期起 YYYY-MM-DD"),
    puzzle_date_to: Optional[str] = Query(None, description="谜题日期止 YYYY-MM-DD"),
    db: AsyncSession = Depends(get_db),
):
    if not token_schema.user_id:
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "未登录",
        )
    date_from = None
    date_to = None
    if puzzle_date_from:
        try:
            date_from = datetime.datetime.strptime(puzzle_date_from, "%Y-%m-%d").date()
        except ValueError:
            pass
    if puzzle_date_to:
        try:
            date_to = datetime.datetime.strptime(puzzle_date_to, "%Y-%m-%d").date()
        except ValueError:
            pass

    single_worker = await get_single_worker(db, SudokuCompletion)
    async with single_worker as worker:
        result = await worker.repository.search_by_user_with_puzzle_filter(
            user_id=token_schema.user_id,
            page_schema=page_schema,
            puzzle_id=puzzle_id,
            puzzle_date_from=date_from,
            puzzle_date_to=date_to,
        )

    data_list = [_row_to_item(row[0], row[1]) for row in result["data"]]
    return success(
        {
            "data": data_list,
            "pagination": result["pagination"],
        }
    )


@router.post("/", response_model=SuccessResponse[dict])
async def record_completion(
    body: SudokuCompletionCreateSchema,
    token_schema: TokenSchema = Depends(get_token),
    db: AsyncSession = Depends(get_db),
):
    if not token_schema.user_id:
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "未登录",
        )
    now = datetime.datetime.now()
    single_worker = await get_single_worker(db, SudokuCompletion)
    async with single_worker as worker:
        instance = await worker.repository.upsert_completion(
            user_id=token_schema.user_id,
            puzzle_id=body.puzzle_id,
            completed_at=now,
            time_seconds=body.time_seconds,
        )
    return success(
        {
            "data": SudokuCompletionItemSchema.model_validate(instance).model_dump(mode="json"),
        }
    )
