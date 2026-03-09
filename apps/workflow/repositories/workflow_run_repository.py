# -*- coding: utf-8 -*-

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

from apps.workflow.models import WorkflowRun


class WorkflowRunRepository(BaseRepository[WorkflowRun]):
    """工作流运行记录 Repository，支持按 run_id、user_id 查询。"""

    name = "workflow_run"

    async def find_by_run_id(
        self,
        run_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[WorkflowRun]:
        """按 run_id 查单条；若传入 user_id 则仅返回该用户的 run。"""
        query = select(WorkflowRun).where(WorkflowRun.run_id == run_id)
        if user_id is not None:
            query = query.where(WorkflowRun.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def list_recent_by_user(self, user_id: str, limit: int = 50) -> List[WorkflowRun]:
        """按 user_id 过滤，按 create_at 降序取最近 limit 条。"""
        query = (
            select(WorkflowRun)
            .where(WorkflowRun.user_id == user_id)
            .order_by(WorkflowRun.create_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
