# -*- coding: utf-8 -*-
# @File    : api/puzzle.py
# @AUTH    : code_creater

import logging
import datetime

from fastapi import APIRouter, Body, Path, Query
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
from ..schemas.sudoku_puzzle import SudokuPuzzleSchema, get_sudoku_puzzle_schema

router = APIRouter()
logger = logging.getLogger("main.apps.sudoku.api.puzzle")

# 仅用于 PATCH 的请求体：只允许更新 puzzle_date、difficulty 等部分字段
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


@router.patch("/{puzzle_id}", response_model=SuccessResponse[SudokuPuzzleResponse])
async def update_puzzle(
    puzzle_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    body: SudokuPuzzleSchema | None = Body(None),
    db: AsyncSession = Depends(get_db),
):
    """更新谜题部分字段（如 puzzle_date、difficulty）。"""
    if body is None:
        body = SudokuPuzzleSchema()

    # 只保留允许更新的字段（保留 None，以支持清空 puzzle_date）
    update_dict = body.model_dump(exclude_unset=True)
    update_dict = {k: v for k, v in update_dict.items() if k in PUZZLE_UPDATE_FIELDS}
    if not update_dict:
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "请提供 puzzle_date 或 difficulty 等可更新字段",
        )
    schema = SudokuPuzzleSchema(**update_dict)

    single_worker = await get_single_worker(db, SudokuPuzzle)
    async with single_worker as worker:
        instance = await worker.repository.update_one(puzzle_id, schema)

    return success({"data": SudokuPuzzleSchema.model_validate(instance)})
