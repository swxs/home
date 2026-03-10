# -*- coding: utf-8 -*-
# @File    : repositories/sudoku_completion_repository.py
# @AUTH    : code_creater

import datetime
from typing import Any, Dict, Optional

from sqlalchemy import func, select

from mysqlengine.repositories import BaseRepository
from web.schemas.pagination import PageSchema, PaginationSchema

# 本模块方法
from ..models.sudoku_completion import SudokuCompletion
from ..models.sudoku_puzzle import SudokuPuzzle


class SudokuCompletionRepository(BaseRepository[SudokuCompletion]):
    name = "sudoku_completion"

    async def find_by_user_and_puzzle(self, user_id: str, puzzle_id: str) -> Optional[SudokuCompletion]:
        stmt = select(SudokuCompletion).where(
            SudokuCompletion.user_id == user_id,
            SudokuCompletion.puzzle_id == puzzle_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def upsert_completion(
        self,
        user_id: str,
        puzzle_id: str,
        completed_at: datetime.datetime,
        time_seconds: Optional[int] = None,
    ) -> SudokuCompletion:
        existing = await self.find_by_user_and_puzzle(user_id, puzzle_id)
        if existing:
            existing.completed_at = completed_at
            existing.time_seconds = time_seconds
            await self.db.flush()
            await self.db.refresh(existing)
            return existing
        instance = SudokuCompletion(
            user_id=user_id,
            puzzle_id=puzzle_id,
            completed_at=completed_at,
            time_seconds=time_seconds,
        )
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def search_by_user_with_puzzle_filter(
        self,
        user_id: str,
        page_schema: PageSchema,
        puzzle_id: Optional[str] = None,
        puzzle_date_from: Optional[datetime.date] = None,
        puzzle_date_to: Optional[datetime.date] = None,
    ) -> Dict[str, Any]:
        """按用户查完成记录，可选按 puzzle_id、谜题日期范围过滤；与 SudokuPuzzle 关联以返回 puzzle_date、difficulty。"""
        Completion = SudokuCompletion
        Puzzle = SudokuPuzzle

        query = (
            select(Completion, Puzzle)
            .select_from(Completion)
            .where(Completion.puzzle_id == Puzzle.id)
            .where(Completion.user_id == user_id)
        )
        count_query = (
            select(func.count())
            .select_from(Completion)
            .where(Completion.puzzle_id == Puzzle.id)
            .where(Completion.user_id == user_id)
        )

        if puzzle_id is not None:
            query = query.where(Completion.puzzle_id == puzzle_id)
            count_query = count_query.where(Completion.puzzle_id == puzzle_id)
        if puzzle_date_from is not None:
            query = query.where(Puzzle.puzzle_date >= puzzle_date_from)
            count_query = count_query.where(Puzzle.puzzle_date >= puzzle_date_from)
        if puzzle_date_to is not None:
            query = query.where(Puzzle.puzzle_date <= puzzle_date_to)
            count_query = count_query.where(Puzzle.puzzle_date <= puzzle_date_to)

        query = query.order_by(Completion.completed_at.desc())

        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        if page_schema.use_pager and page_schema.limit > 0:
            query = query.offset(page_schema.skip).limit(page_schema.limit)

        result = await self.db.execute(query)
        rows = result.all()

        pagination = PaginationSchema(
            total=total,
            order_by=page_schema.order_by,
            use_pager=page_schema.use_pager,
            page=page_schema.page,
            page_number=page_schema.page_number,
        )

        return {
            "data": rows,
            "pagination": pagination,
        }
