# -*- coding: utf-8 -*-
# @File    : services/sudoku_completion_service.py
# @AUTH    : code_creater

import logging
import datetime
from typing import Any, Dict, Optional

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from home.web.schemas.types import objectId
from home.web.dependencies.session import get_session, transaction

from home.web.exceptions import Http400BadRequestException
from home.web.schemas.pagination import PageSchema

# 本模块方法
from ..repositories.sudoku_completion_repository import SudokuCompletionRepository
from ..schemas.sudoku_completion import (
    SudokuCompletionCreateSchema,
    SudokuCompletionItemSchema,
)

logger = logging.getLogger("main.apps.sudoku.services.sudoku_completion_service")


def _row_to_item(completion, puzzle) -> dict:
    item = SudokuCompletionItemSchema.model_validate(completion).model_dump(mode="json")
    if puzzle is not None:
        item["puzzle_date"] = getattr(puzzle, "puzzle_date", None)
        item["difficulty"] = getattr(puzzle, "difficulty", None)
        if item["difficulty"] is not None and hasattr(item["difficulty"], "value"):
            item["difficulty"] = item["difficulty"].value
    return item


class SudokuCompletionService:
    """数独完成记录业务层：登录校验、查询编排、upsert 与事务边界。"""

    def __init__(self, session: AsyncSession, repo: Optional[SudokuCompletionRepository] = None):
        self.session = session
        self.repo = repo or SudokuCompletionRepository(session)

    async def list_my(
        self,
        user_id: objectId,
        page_schema: PageSchema,
        puzzle_id: Optional[objectId] = None,
        puzzle_date_from: Optional[str] = None,
        puzzle_date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not user_id:
            raise Http400BadRequestException(
                Http400BadRequestException.IllegalArgument,
                "未登录",
            )
        date_from = None
        date_to = None
        if puzzle_date_from:
            try:
                date_from = datetime.datetime.strptime(puzzle_date_from, "%Y-%m-%d").date()
            except ValueError:
                pass
        if puzzle_date_to:
            try:
                date_to = datetime.datetime.strptime(puzzle_date_to, "%Y-%m-%d").date()
            except ValueError:
                pass

        result = await self.repo.search_by_user_with_puzzle_filter(
            user_id=user_id,
            page_schema=page_schema,
            puzzle_id=puzzle_id,
            puzzle_date_from=date_from,
            puzzle_date_to=date_to,
        )

        data_list = [_row_to_item(row[0], row[1]) for row in result["data"]]
        return {
            "data": data_list,
            "pagination": result["pagination"],
        }

    async def record(self, user_id: objectId, body: SudokuCompletionCreateSchema) -> dict:
        if not user_id:
            raise Http400BadRequestException(
                Http400BadRequestException.IllegalArgument,
                "未登录",
            )
        now = datetime.datetime.now()
        async with transaction(self.session):
            instance = await self.repo.upsert_completion(
                user_id=user_id,
                puzzle_id=body.puzzle_id,
                completed_at=now,
                time_seconds=body.time_seconds,
            )

        return SudokuCompletionItemSchema.model_validate(instance).model_dump(mode="json")


async def get_sudoku_completion_service(session: AsyncSession = Depends(get_session)) -> SudokuCompletionService:
    return SudokuCompletionService(session)
