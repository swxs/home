# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from apps.workflow.consts import WorkflowRunStatus


class WorkflowRunCreateSchema(BaseModel):
    """创建运行记录时使用。user_id/workflow_id 为 ObjectId 字符串；status 为 IntEnum 值。"""

    run_id: str = Field(..., description="UUID")
    workflow_id: str = Field(..., description="工作流 ID（ObjectId 字符串）")
    user_id: str = Field(..., description="发起运行的用户 ID（ObjectId 字符串）")
    status: int = Field(default=WorkflowRunStatus.RUNNING, description="状态 0=running 1=succeeded 2=failed")
    inputs: Optional[Dict[str, Any]] = Field(default_factory=dict, description="入参")


class WorkflowRunUpdateSchema(BaseModel):
    """更新运行结果时使用，仅包含需更新字段。status 为 IntEnum 值。"""

    status: Optional[int] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
