# -*- coding: utf-8 -*-
# @File    : repositories/sudoku_puzzle_repository.py
# @AUTH    : code_creater

import datetime
from typing import Optional

from sqlalchemy import select

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.sudoku_puzzle import SudokuPuzzle


class SudokuPuzzleRepository(BaseRepository[SudokuPuzzle]):
    model = SudokuPuzzle
    name = "sudoku_puzzle"

    async def find_by_date(self, puzzle_date: datetime.date) -> Optional[SudokuPuzzle]:
        stmt = select(SudokuPuzzle).where(SudokuPuzzle.puzzle_date == puzzle_date).limit(1)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
