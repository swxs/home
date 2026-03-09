# -*- coding: utf-8 -*-

from enum import IntEnum


# 工作流运行状态，IntEnum 值需在 -128～127
class WorkflowRunStatus(IntEnum):
    RUNNING = 1
    SUCCEEDED = 2
    FAILED = 3


# 预注册工作流 ID 使用合法 ObjectId（24 位十六进制）
WORKFLOW_ID_ECHO = "000000000000000000000001"
WORKFLOW_ID_SUMMARIZE = "000000000000000000000002"
WORKFLOW_ID_CALCULATOR = "000000000000000000000003"
