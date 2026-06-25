# -*- coding: utf-8 -*-
# @File    : api/completion.py
# @AUTH    : code_creater

import logging
from typing import Optional

from fastapi import APIRouter, Query
from fastapi.param_functions import Depends

from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.response import SudokuCompletionSearchResponse
from ..schemas.sudoku_completion import SudokuCompletionCreateSchema
from ..services.sudoku_completion_service import (
    SudokuCompletionService,
    get_sudoku_completion_service,
)

router = APIRouter()
logger = logging.getLogger("main.apps.sudoku.api.completion")


@router.get("/me", response_model=SuccessResponse[SudokuCompletionSearchResponse])
async def get_my_completions(
    token_schema: TokenSchema = Depends(get_token),
    page_schema: PageSchema = Depends(get_pagination),
    puzzle_id: Optional[str] = Query(None, description="谜题ID"),
    puzzle_date_from: Optional[str] = Query(None, description="谜题日期起 YYYY-MM-DD"),
    puzzle_date_to: Optional[str] = Query(None, description="谜题日期止 YYYY-MM-DD"),
    service: SudokuCompletionService = Depends(get_sudoku_completion_service),
):
    result = await service.list_my(
        user_id=token_schema.user_id,
        page_schema=page_schema,
        puzzle_id=puzzle_id,
        puzzle_date_from=puzzle_date_from,
        puzzle_date_to=puzzle_date_to,
    )
    return success(result)


@router.post("/", response_model=SuccessResponse[dict])
async def record_completion(
    body: SudokuCompletionCreateSchema,
    token_schema: TokenSchema = Depends(get_token),
    service: SudokuCompletionService = Depends(get_sudoku_completion_service),
):
    item = await service.record(token_schema.user_id, body)
    return success({"data": item})
