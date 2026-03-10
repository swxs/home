# -*- coding: utf-8 -*-
# @FILE    : schemas/sudoku_completion.py
# @AUTH    : code_creater

import datetime
from typing import Optional

from fastapi import Query
from pydantic import field_validator

from web.schemas import BaseSchema


class SudokuCompletionCreateSchema(BaseSchema):
    """记录完成请求 body"""

    puzzle_id: str
    time_seconds: Optional[int] = None

    @field_validator("puzzle_id")
    @classmethod
    def validate_puzzle_id(cls, v: str) -> str:
        if not v or len(v) != 24:
            raise ValueError("puzzle_id 必须为 24 位十六进制")
        valid = set("0123456789abcdefABCDEF")
        if not all(c in valid for c in v):
            raise ValueError("puzzle_id 必须为 24 位十六进制")
        return v


class SudokuCompletionQuerySchema(BaseSchema):
    """我的完成列表查询（用于 search schema 的 filter_dict）"""

    user_id: Optional[str] = None
    puzzle_id: Optional[str] = None


class SudokuCompletionItemSchema(BaseSchema):
    """单条完成记录（含可选谜题摘要）"""

    id: Optional[str] = None
    user_id: Optional[str] = None
    puzzle_id: Optional[str] = None
    completed_at: Optional[datetime.datetime] = None
    time_seconds: Optional[int] = None
    puzzle_date: Optional[datetime.date] = None
    difficulty: Optional[int] = None


async def get_completion_query_schema(
    puzzle_id: Optional[str] = Query(None, description="谜题ID"),
):
    """GET /completions/me 的 Query 仅含 puzzle_id；日期范围在 API 中单独传参。"""
    return SudokuCompletionQuerySchema(puzzle_id=puzzle_id)
