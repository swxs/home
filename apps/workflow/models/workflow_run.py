# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional

from sqlalchemy import Index, String, Text
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel
from mysqlengine.fields import IntEnumType, ObjectIdType

from apps.workflow.consts import WorkflowRunStatus


class WorkflowRun(baseModel):
    """工作流运行记录，按 user_id 隔离。"""

    __tablename__ = "workflow_run"
    __table_args__ = (
        Index("ix_workflow_run_user_id", "user_id"),
        Index("ix_workflow_run_user_id", "run_id"),
    )

    user_id: Mapped[str] = mapped_column(
        ObjectIdType,
        nullable=False,
        index=True,
        comment="发起运行的用户 ID",
    )
    run_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        unique=True,
        comment="对外 API 使用的 UUID",
    )
    workflow_id: Mapped[str] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="工作流 ID",
    )
    status: Mapped[int] = mapped_column(
        IntEnumType(choice=WorkflowRunStatus),
        nullable=False,
        default=WorkflowRunStatus.RUNNING,
        comment="0=running 1=succeeded 2=failed",
    )
    inputs: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        comment="入参",
    )
    output: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        comment="执行成功时的输出",
    )
    error: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="执行失败时的错误信息",
    )
