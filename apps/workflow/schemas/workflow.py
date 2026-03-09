# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class WorkflowItemSchema(BaseModel):
    """工作流列表项。"""

    id: str = Field(..., description="工作流 ID")
    name: str = Field(..., description="显示名称")
    description: str = Field(default="", description="描述")
    input_schema: Optional[Dict[str, Any]] = Field(default=None, description="输入参数 schema")


class WorkflowListResponse(BaseModel):
    """GET /workflows 响应。"""

    items: List[WorkflowItemSchema] = Field(default_factory=list)


class WorkflowRunRequest(BaseModel):
    """POST /workflows/{id}/run 请求体。"""

    inputs: Dict[str, Any] = Field(default_factory=dict, description='工作流输入，如 {"message": "..."}')


class WorkflowRunResponse(BaseModel):
    """POST /workflows/{id}/run 同步执行响应。"""

    output: Dict[str, Any] = Field(default_factory=dict, description="工作流输出")
    status: str = Field(default="succeeded", description="succeeded | failed")
    run_id: Optional[str] = Field(default=None, description="本次运行的记录 ID，同步也会落库")


class WorkflowRunAsyncResponse(BaseModel):
    """POST /workflows/{id}/run?async=1 异步执行响应。"""

    run_id: str = Field(..., description="运行 ID，用于 GET /runs/{run_id} 轮询")
    status: str = Field(default="running", description="running")
