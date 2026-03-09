# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.schemas.token import TokenSchema, get_token

from apps.workflow.models import WorkflowRun
from apps.workflow.services.run_store import get_run, list_runs

router = APIRouter()


@router.get("")
async def list_runs_endpoint(
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    token_schema: TokenSchema = Depends(get_token),
):
    """列出当前用户运行历史（最近 N 条）。"""
    if not token_schema.user_id:
        raise HTTPException(status_code=401, detail="user_id required")
    single_worker = await get_single_worker(db, WorkflowRun)
    async with single_worker as worker:
        items = await list_runs(worker.repository, token_schema.user_id, limit=limit)
    return {"items": items}


@router.get("/{run_id}")
async def get_run_endpoint(
    run_id: str,
    db: AsyncSession = Depends(get_db),
    token_schema: TokenSchema = Depends(get_token),
):
    """查询某次执行的状态与结果（仅当前用户的 run）。"""
    if not token_schema.user_id:
        raise HTTPException(status_code=401, detail="user_id required")
    single_worker = await get_single_worker(db, WorkflowRun)
    async with single_worker as worker:
        record = await get_run(worker.repository, run_id, token_schema.user_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
    return record
