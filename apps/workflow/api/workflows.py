# -*- coding: utf-8 -*-

import asyncio

from fastapi import APIRouter, HTTPException, Query
from fastapi.param_functions import Depends
from langchain_core.messages import HumanMessage
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.schemas.token import TokenSchema, get_token

from apps.workflow.consts import (
    WORKFLOW_ID_CALCULATOR,
    WORKFLOW_ID_ECHO,
    WORKFLOW_ID_SUMMARIZE,
)
from apps.workflow.graphs import list_registered_workflow_ids
from apps.workflow.models import WorkflowRun
from apps.workflow.schemas.workflow import (
    WorkflowItemSchema,
    WorkflowListResponse,
    WorkflowRunAsyncResponse,
    WorkflowRunRequest,
    WorkflowRunResponse,
)
from apps.workflow.services.executor import run_workflow
from apps.workflow.services.run_store import create_run, set_run_result

router = APIRouter()

# 工作流 input_schema 约定：properties 下每字段含 type、title（前端 label）、description（前端 placeholder）
WORKFLOW_META = {
    WORKFLOW_ID_ECHO: WorkflowItemSchema(
        id=WORKFLOW_ID_ECHO,
        name="Echo",
        description="最小示例：将输入 text 原样输出，无需 LLM。",
        input_schema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "title": "输入",
                    "description": "输入内容，Echo 工作流将原样输出",
                },
            },
            "required": ["text"],
        },
    ),
    WORKFLOW_ID_SUMMARIZE: WorkflowItemSchema(
        id=WORKFLOW_ID_SUMMARIZE,
        name="文本总结",
        description="通过 LLM 总结输入文本的关键信息。",
        input_schema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "title": "待总结文本",
                    "description": "输入需要总结的文本内容",
                },
            },
            "required": ["text"],
        },
    ),
    WORKFLOW_ID_CALCULATOR: WorkflowItemSchema(
        id=WORKFLOW_ID_CALCULATOR,
        name="计算器助手",
        description="根据你的问题决定是否使用计算器并给出回答，支持数学计算与一般问答。",
        input_schema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "title": "问题",
                    "description": "例如 (100+50)*3 等于多少？或 什么是人工智能？",
                },
            },
            "required": ["text"],
        },
    ),
}


@router.get("", response_model=WorkflowListResponse)
async def list_workflows():
    """列出可用的工作流。"""
    ids = list_registered_workflow_ids()
    items = [WORKFLOW_META[w_id] for w_id in ids if w_id in WORKFLOW_META]
    return WorkflowListResponse(items=items)


async def _run_workflow_background(run_id: str, workflow_id: str, inputs: dict) -> None:
    """后台执行工作流并写入 DB。"""
    try:
        output = await run_workflow(workflow_id, inputs)
        await set_run_result(run_id, output=output, error=None)
    except Exception as e:
        await set_run_result(run_id, output=None, error=str(e))


def _normalize_inputs(workflow_id: str, inputs: dict) -> dict:
    """计算器 Agent 需要完整初始 state（query + messages 含首条用户问题）。"""
    if workflow_id != WORKFLOW_ID_CALCULATOR:
        return inputs
    query = inputs.get("text", "").strip()
    return {
        "query": query,
        "messages": [HumanMessage(content=query)],
        "tool_results": [],
        "answer": "",
    }


@router.post("/{workflow_id}/run", response_model=WorkflowRunResponse | WorkflowRunAsyncResponse)
async def run_workflow_endpoint(
    workflow_id: str,
    body: WorkflowRunRequest,
    async_run: bool = Query(False, alias="async", description="是否异步执行，返回 run_id 供轮询"),
    db: AsyncSession = Depends(get_db),
    token_schema: TokenSchema = Depends(get_token),
):
    """执行指定工作流。async=1 时异步执行并返回 run_id，否则同步返回输出。"""
    if workflow_id not in WORKFLOW_META:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {workflow_id}")
    if not token_schema.user_id:
        raise HTTPException(status_code=401, detail="user_id required")
    inputs = _normalize_inputs(workflow_id, body.inputs)
    if async_run:
        single_worker = await get_single_worker(db, WorkflowRun)
        async with single_worker as worker:
            run_id = await create_run(worker.repository, workflow_id, inputs, token_schema.user_id)
        asyncio.create_task(_run_workflow_background(run_id, workflow_id, inputs))
        return WorkflowRunAsyncResponse(run_id=run_id, status="running")
    # 同步执行也落库：先创建 run 记录，再执行，最后更新结果
    single_worker = await get_single_worker(db, WorkflowRun)
    async with single_worker as worker:
        run_id = await create_run(worker.repository, workflow_id, inputs, token_schema.user_id)
    try:
        output = await run_workflow(workflow_id, inputs)
        await set_run_result(run_id, output=output, error=None)
        return WorkflowRunResponse(output=output, status="succeeded", run_id=run_id)
    except Exception as e:
        await set_run_result(run_id, output=None, error=str(e))
        return WorkflowRunResponse(output={"error": str(e)}, status="failed", run_id=run_id)
