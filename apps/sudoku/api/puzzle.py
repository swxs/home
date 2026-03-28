# -*- coding: utf-8 -*-
# @File    : api/puzzle.py
# @AUTH    : code_creater

import logging
import datetime
from typing import Annotated

from fastapi import APIRouter, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import SuccessResponse

# 本模块方法
from ..models.sudoku_puzzle import SudokuPuzzle
from ..schemas.response import (
    SudokuPuzzleResponse,
    SudokuPuzzleSearchResponse,
)
from ..schemas.sudoku_puzzle import (
    SudokuPuzzleCreateBody,
    SudokuPuzzlePatchBody,
    SudokuPuzzleSchema,
    get_sudoku_puzzle_schema,
)
from ..utils.sudoku_solver import solve_unique_solution
from ..utils.sudoku_validator import is_valid_sudoku_grid

router = APIRouter()
logger = logging.getLogger("main.apps.sudoku.api.puzzle")

PUZZLE_UPDATE_FIELDS = {"puzzle_date", "difficulty"}


@router.get("/", response_model=SuccessResponse[SudokuPuzzleSearchResponse])
async def list_puzzles(
    schema: SudokuPuzzleSchema = Depends(get_sudoku_puzzle_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, SudokuPuzzle)
    async with single_worker as worker:
        result = await worker.repository.search(schema, page_schema)

    return success(
        {
            "data": [SudokuPuzzleSchema.model_validate(p) for p in result["data"]],
            "pagination": result["pagination"],
        }
    )


@router.post("/", response_model=SuccessResponse[SudokuPuzzleResponse])
async def create_puzzle(
    body: SudokuPuzzleCreateBody,
    db: AsyncSession = Depends(get_db),
):
    """手动录入题目（可选日期、难度）；未传 solution 时服务端求唯一解。"""
    puzzle = body.puzzle
    if body.solution is not None:
        solution = body.solution
    else:
        try:
            solution = solve_unique_solution(puzzle)
        except ValueError as e:
            raise Http400BadRequestException(
                Http400BadRequestException.IllegalArgument,
                str(e),
            )
    if not is_valid_sudoku_grid(solution):
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "答案不是合法数独解",
        )
    puzzle_date = body.puzzle_date if body.puzzle_date is not None else datetime.date.today()
    schema = SudokuPuzzleSchema(
        puzzle=puzzle,
        solution=solution,
        puzzle_date=puzzle_date,
        difficulty=body.difficulty,
    )
    single_worker = await get_single_worker(db, SudokuPuzzle)
    async with single_worker as worker:
        instance = await worker.repository.create_one(schema)
    return success({"data": SudokuPuzzleSchema.model_validate(instance)})


@router.patch("/{puzzle_id}", response_model=SuccessResponse[SudokuPuzzleResponse])
async def update_puzzle(
    puzzle_id: Annotated[str, Path(regex="[0-9a-fA-F]{24}")],
    body: SudokuPuzzlePatchBody,
    db: AsyncSession = Depends(get_db),
):
    """更新谜题日期、难度（可按字段部分更新；显式 null 可清空）。"""
    to_apply = PUZZLE_UPDATE_FIELDS & body.model_fields_set
    if not to_apply:
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "请提供 puzzle_date 或 difficulty",
        )
    single_worker = await get_single_worker(db, SudokuPuzzle)
    async with single_worker as worker:
        instance = await worker.repository.find_one(puzzle_id)
        if instance is None:
            raise Http400BadRequestException(
                Http400BadRequestException.NoResource,
                "对象不存在",
            )
        for name in to_apply:
            setattr(instance, name, getattr(body, name))
        await worker.db.flush()
        await worker.db.refresh(instance)
    return success({"data": SudokuPuzzleSchema.model_validate(instance)})


@router.get("/by-date", response_model=SuccessResponse[SudokuPuzzleResponse])
async def get_puzzle_by_date(
    date: str = Query(..., description="日期 YYYYMMDD"),
    db: AsyncSession = Depends(get_db),
):
    try:
        d = datetime.datetime.strptime(date.strip(), "%Y%m%d").date()
    except ValueError:
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "日期格式应为 YYYYMMDD",
        )

    single_worker = await get_single_worker(db, SudokuPuzzle)
    async with single_worker as worker:
        instance = await worker.repository.find_by_date(d)

    if instance is None:
        raise Http400BadRequestException(
            Http400BadRequestException.NoResource,
            "该日期暂无谜题",
        )

    return success({"data": SudokuPuzzleSchema.model_validate(instance)})


@router.get("/{puzzle_id}", response_model=SuccessResponse[SudokuPuzzleResponse])
async def get_puzzle(
    puzzle_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, SudokuPuzzle)
    async with single_worker as worker:
        instance = await worker.repository.find_one(puzzle_id)

    if instance is None:
        raise Http400BadRequestException(
            Http400BadRequestException.NoResource,
            "谜题不存在",
        )

    return success({"data": SudokuPuzzleSchema.model_validate(instance)})
