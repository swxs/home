# -*- coding: utf-8 -*-
# @FILE    : models/sudoku_puzzle.py
# @AUTH    : code_creater

import datetime
from typing import Optional

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from home.mysqlengine import baseModel
from home.mysqlengine.fields import IntEnumType

# 本模块方法
from .. import consts


class SudokuPuzzle(baseModel):
    __tablename__ = "sudoku_puzzle"

    puzzle: Mapped[str] = mapped_column(
        String(81),
        nullable=False,
        comment="题目，81 位，0 表示空格，1-9 表示已知格，行优先",
    )
    solution: Mapped[str] = mapped_column(
        String(81),
        nullable=False,
        comment="答案，81 位全为 1-9，行优先",
    )
    puzzle_date: Mapped[Optional[datetime.date]] = mapped_column(
        Date,
        nullable=True,
        comment="谜题日期，用于每日一题",
    )
    difficulty: Mapped[Optional[consts.Difficulty]] = mapped_column(
        IntEnumType(consts.Difficulty),
        nullable=True,
        comment="难度",
    )
