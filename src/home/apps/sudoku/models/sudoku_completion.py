# -*- coding: utf-8 -*-
# @FILE    : models/sudoku_completion.py
# @AUTH    : code_creater

import datetime
from typing import Optional

from sqlalchemy import Index, Integer, UniqueConstraint
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from home.mysqlengine import baseModel
from home.mysqlengine.fields import ObjectIdType
from home.web.schemas.types import objectId


class SudokuCompletion(baseModel):
    """用户数独完成记录：同一用户同一题仅一条。"""

    __tablename__ = "sudoku_completion"

    user_id: Mapped[objectId] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="用户ID",
    )
    puzzle_id: Mapped[str] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="谜题ID",
    )
    completed_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME(fsp=6),
        nullable=False,
        comment="完成时间",
    )
    time_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="用时（秒）",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "puzzle_id", name="uq_sudoku_completion_user_puzzle"),
        Index("idx_sudoku_completion_user_id", "user_id"),
    )
