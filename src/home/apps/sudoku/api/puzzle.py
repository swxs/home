# -*- coding: utf-8 -*-
# @File    : api/puzzle.py
# @AUTH    : code_creater

import logging
from typing import Annotated

from fastapi import APIRouter, Path, Query
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.pagination import PageSchema, get_pagination
from home.web.schemas.response import SuccessResponse

# 本模块方法
from ..schemas.response import (
    SudokuPuzzleResponse,
    SudokuPuzzleSearchResponse,
)
from ..schemas.sudoku_puzzle import (
    SudokuPuzzleCreateBody,
    SudokuPuzzleFilter,
    SudokuPuzzlePatchBody,
    get_sudoku_puzzle_filter,
)
from ..services.sudoku_puzzle_service import (
    SudokuPuzzleService,
    get_sudoku_puzzle_service,
)

router = APIRouter()
logger = logging.getLogger("main.apps.sudoku.api.puzzle")


@router.get("/", response_model=SuccessResponse[SudokuPuzzleSearchResponse])
async def list_puzzles(
    schema: SudokuPuzzleFilter = Depends(get_sudoku_puzzle_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: SudokuPuzzleService = Depends(get_sudoku_puzzle_service),
):
    result = await service.list(schema, page_schema)
    return success(result)


@router.post("/", response_model=SuccessResponse[SudokuPuzzleResponse])
async def create_puzzle(
    body: SudokuPuzzleCreateBody,
    service: SudokuPuzzleService = Depends(get_sudoku_puzzle_service),
):
    """手动录入题目（可选日期、难度）；未传 solution 时服务端求唯一解。"""
    instance = await service.create(body)
    return success({"data": instance})


@router.patch("/{puzzle_id}", response_model=SuccessResponse[SudokuPuzzleResponse])
async def update_puzzle(
    puzzle_id: Annotated[str, Path(regex="[0-9a-fA-F]{24}")],
    body: SudokuPuzzlePatchBody,
    service: SudokuPuzzleService = Depends(get_sudoku_puzzle_service),
):
    """更新谜题日期、难度（可按字段部分更新；显式 null 可清空）。"""
    instance = await service.update(puzzle_id, body)
    return success({"data": instance})


@router.get("/by-date", response_model=SuccessResponse[SudokuPuzzleResponse])
async def get_puzzle_by_date(
    date: str = Query(..., description="日期 YYYYMMDD"),
    service: SudokuPuzzleService = Depends(get_sudoku_puzzle_service),
):
    instance = await service.get_by_date(date)
    return success({"data": instance})


@router.get("/{puzzle_id}", response_model=SuccessResponse[SudokuPuzzleResponse])
async def get_puzzle(
    puzzle_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: SudokuPuzzleService = Depends(get_sudoku_puzzle_service),
):
    instance = await service.get(puzzle_id)
    return success({"data": instance})
