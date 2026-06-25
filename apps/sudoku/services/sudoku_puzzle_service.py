# -*- coding: utf-8 -*-
# @File    : services/sudoku_puzzle_service.py
# @AUTH    : code_creater

import logging
import datetime
from typing import Any, Dict

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.schemas.pagination import PageSchema

# 本模块方法
from ..models.sudoku_puzzle import SudokuPuzzle
from ..schemas.sudoku_puzzle import (
    SudokuPuzzleCreateBody,
    SudokuPuzzleFilter,
    SudokuPuzzleOut,
    SudokuPuzzlePatchBody,
    SudokuPuzzleSchema,
)
from ..utils.sudoku_solver import solve_unique_solution
from ..utils.sudoku_validator import is_valid_sudoku_grid

logger = logging.getLogger("main.apps.sudoku.services.sudoku_puzzle_service")

PUZZLE_UPDATE_FIELDS = {"puzzle_date", "difficulty"}


class SudokuPuzzleService:
    """数独谜题业务层：求解/校验领域编排、CRUD 与事务边界。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, filter_schema: SudokuPuzzleFilter, page_schema: PageSchema) -> Dict[str, Any]:
        single_worker = await get_single_worker(self.db, SudokuPuzzle)
        async with single_worker as worker:
            result = await worker.repository.search(filter_schema, page_schema)

        return {
            "data": [SudokuPuzzleOut.model_validate(p) for p in result["data"]],
            "pagination": result["pagination"],
        }

    async def create(self, body: SudokuPuzzleCreateBody) -> SudokuPuzzleOut:
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
        single_worker = await get_single_worker(self.db, SudokuPuzzle)
        async with single_worker as worker:
            instance = await worker.repository.create_one(schema)

        return SudokuPuzzleOut.model_validate(instance)

    async def update(self, puzzle_id: str, body: SudokuPuzzlePatchBody) -> SudokuPuzzleOut:
        """更新谜题日期、难度（可按字段部分更新；显式 null 可清空）。"""
        to_apply = PUZZLE_UPDATE_FIELDS & body.model_fields_set
        if not to_apply:
            raise Http400BadRequestException(
                Http400BadRequestException.IllegalArgument,
                "请提供 puzzle_date 或 difficulty",
            )
        single_worker = await get_single_worker(self.db, SudokuPuzzle)
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

        return SudokuPuzzleOut.model_validate(instance)

    async def get_by_date(self, date: str) -> SudokuPuzzleOut:
        try:
            d = datetime.datetime.strptime(date.strip(), "%Y%m%d").date()
        except ValueError:
            raise Http400BadRequestException(
                Http400BadRequestException.IllegalArgument,
                "日期格式应为 YYYYMMDD",
            )

        single_worker = await get_single_worker(self.db, SudokuPuzzle)
        async with single_worker as worker:
            instance = await worker.repository.find_by_date(d)

        if instance is None:
            raise Http400BadRequestException(
                Http400BadRequestException.NoResource,
                "该日期暂无谜题",
            )

        return SudokuPuzzleOut.model_validate(instance)

    async def get(self, puzzle_id: str) -> SudokuPuzzleOut:
        single_worker = await get_single_worker(self.db, SudokuPuzzle)
        async with single_worker as worker:
            instance = await worker.repository.find_one(puzzle_id)

        if instance is None:
            raise Http400BadRequestException(
                Http400BadRequestException.NoResource,
                "谜题不存在",
            )

        return SudokuPuzzleOut.model_validate(instance)


async def get_sudoku_puzzle_service(db: AsyncSession = Depends(get_db)) -> SudokuPuzzleService:
    return SudokuPuzzleService(db)
