# -*- coding: utf-8 -*-
# @FILE    : schemas/sudoku_puzzle.py
# @AUTH    : model_creater

import datetime
from typing import Optional

from fastapi import Query
from pydantic import field_serializer, field_validator, model_validator

from web.schemas import BaseSchema

# 日期格式：创建/修改请求与响应统一为 YYYY/MM/DD
PUZZLE_DATE_FMT = "%Y/%m/%d"


def _check_puzzle_chars(s: str) -> None:
    if len(s) != 81:
        raise ValueError("puzzle 必须为 81 个字符")
    valid = set("0123456789")
    for i, c in enumerate(s):
        if c not in valid:
            raise ValueError(f"puzzle 第 {i + 1} 位非法字符: {c}")


def _check_solution_chars(s: str) -> None:
    if len(s) != 81:
        raise ValueError("solution 必须为 81 个字符")
    valid = set("123456789")
    for i, c in enumerate(s):
        if c not in valid:
            raise ValueError(f"solution 第 {i + 1} 位非法字符: {c}")


class SudokuPuzzleSchema(BaseSchema):
    puzzle: Optional[str] = None
    solution: Optional[str] = None
    puzzle_date: Optional[datetime.date] = None
    difficulty: Optional[int] = None

    @field_validator("puzzle_date", mode="before")
    @classmethod
    def parse_puzzle_date(cls, v: Optional[str | datetime.date]) -> Optional[datetime.date]:
        if v is None:
            return None
        if isinstance(v, datetime.date):
            return v
        s = (v or "").strip().replace("-", "/")
        if not s:
            return None
        return datetime.datetime.strptime(s, PUZZLE_DATE_FMT).date()

    @field_serializer("puzzle_date")
    def serialize_puzzle_date(self, v: Optional[datetime.date]) -> Optional[str]:
        if v is None:
            return None
        return v.strftime(PUZZLE_DATE_FMT)

    @field_validator("puzzle")
    @classmethod
    def validate_puzzle(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        _check_puzzle_chars(v)
        if "0" not in v:
            raise ValueError("puzzle 至少需要有一个空格（0）")
        return v

    @field_validator("solution")
    @classmethod
    def validate_solution(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        _check_solution_chars(v)
        return v

    @model_validator(mode="after")
    def puzzle_solution_consistent(self):
        if self.puzzle is not None and self.solution is not None:
            for i, (p, s) in enumerate(zip(self.puzzle, self.solution)):
                if p != "0" and p != s:
                    raise ValueError(f"第 {i + 1} 位：puzzle 已知格与 solution 不一致")
        return self


async def get_sudoku_puzzle_schema(
    puzzle_date: Optional[str] = Query(None, description="谜题日期 YYYY/MM/DD"),
    difficulty: Optional[int] = Query(None),
):
    params = {}
    if puzzle_date is not None:
        try:
            s = puzzle_date.strip().replace("-", "/")
            params["puzzle_date"] = datetime.datetime.strptime(s, PUZZLE_DATE_FMT).date()
        except ValueError:
            pass
    if difficulty is not None:
        params["difficulty"] = difficulty
    return SudokuPuzzleSchema(**params)
