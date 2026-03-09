# -*- coding: utf-8 -*-
"""
运行记录持久化：基于 DB 的 create/get/list，后台任务内独立 session 更新结果。
"""

import uuid
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine import SessionLocal
from mysqlengine.repositories import BaseRepository

from apps.workflow.consts import WorkflowRunStatus
from apps.workflow.models import WorkflowRun
from apps.workflow.repositories.workflow_run_repository import WorkflowRunRepository
from apps.workflow.schemas.workflow_run import (
    WorkflowRunCreateSchema,
    WorkflowRunUpdateSchema,
)

_STATUS_TO_STR = {
    WorkflowRunStatus.RUNNING: "running",
    WorkflowRunStatus.SUCCEEDED: "succeeded",
    WorkflowRunStatus.FAILED: "failed",
}


def _row_to_dict(row: WorkflowRun) -> Dict[str, Any]:
    """将 ORM 转为与当前 API 一致的 dict。status 从 IntEnum 转为字符串。"""
    status_val = getattr(row, "status", None)
    status_str = _STATUS_TO_STR.get(status_val, "running") if status_val is not None else "running"
    return {
        "run_id": row.run_id,
        "workflow_id": row.workflow_id,
        "status": status_str,
        "output": row.output,
        "error": row.error,
        "created_at": row.create_at.isoformat() if row.create_at else None,
    }


async def create_run(
    repo: BaseRepository[WorkflowRun],
    workflow_id: str,
    inputs: Dict[str, Any],
    user_id: str,
) -> str:
    """创建一条运行记录，状态为 running，返回 run_id。调用方负责 commit（如通过 single_worker 上下文）。"""
    run_id = str(uuid.uuid4())
    schema = WorkflowRunCreateSchema(
        run_id=run_id,
        workflow_id=workflow_id,
        user_id=user_id,
        status=WorkflowRunStatus.RUNNING,
        inputs=inputs,
    )
    await repo.create_one(schema)
    return run_id


async def set_run_result(
    run_id: str,
    output: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
) -> None:
    """更新运行结果。在独立 session 内执行，供后台任务调用。"""
    async with SessionLocal() as session:
        repo = WorkflowRunRepository(WorkflowRun, session)
        row = await repo.find_by_run_id(run_id, user_id=None)
        if not row:
            return
        schema = WorkflowRunUpdateSchema(
            status=WorkflowRunStatus.FAILED if error else WorkflowRunStatus.SUCCEEDED,
            output=output,
            error=error,
        )
        await repo.update_one(str(row.id), schema)
        await session.commit()


async def get_run(
    repo: WorkflowRunRepository,
    run_id: str,
    user_id: str,
) -> Optional[Dict[str, Any]]:
    """查询当前用户的运行记录，无则返回 None。"""
    row = await repo.find_by_run_id(run_id, user_id=user_id)
    if not row:
        return None
    return _row_to_dict(row)


async def list_runs(
    repo: WorkflowRunRepository,
    user_id: str,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """列出当前用户最近运行记录。"""
    rows = await repo.list_recent_by_user(user_id, limit=limit)
    return [_row_to_dict(r) for r in rows]
