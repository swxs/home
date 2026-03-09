# -*- coding: utf-8 -*-
"""
工作流图注册表。一期为预注册图（方式 A）；二期可接入方式 B：从 DB/配置文件加载并动态构建 StateGraph。
"""

from apps.workflow.consts import (
    WORKFLOW_ID_CALCULATOR,
    WORKFLOW_ID_ECHO,
    WORKFLOW_ID_SUMMARIZE,
)

# 本模块方法
from .calculator import build_calculator_graph
from .echo import build_echo_graph
from .summarize import build_summarize_graph

# 预注册工作流：workflow_id -> 编译后的图（懒加载，首次请求时编译）
_REGISTRY = {}

# 方式 B 扩展点：可从 DB 或 YAML/JSON 读取工作流定义，在此处调用 build_graph_from_config(config) 注册
# 示例：def build_graph_from_config(config: dict) -> CompiledGraph: ...


def get_graph(workflow_id: str):
    """根据 workflow_id 获取已编译的 LangGraph 图。"""
    if workflow_id not in _REGISTRY:
        if workflow_id == WORKFLOW_ID_ECHO:
            _REGISTRY[workflow_id] = build_echo_graph()
        elif workflow_id == WORKFLOW_ID_SUMMARIZE:
            _REGISTRY[workflow_id] = build_summarize_graph()
        elif workflow_id == WORKFLOW_ID_CALCULATOR:
            _REGISTRY[workflow_id] = build_calculator_graph()
        else:
            raise KeyError(f"Unknown workflow_id: {workflow_id!r}")
    return _REGISTRY[workflow_id]


def list_registered_workflow_ids():
    """返回所有已注册的 workflow_id（用于列表接口），使用合法 ObjectId。"""
    return [WORKFLOW_ID_ECHO, WORKFLOW_ID_SUMMARIZE, WORKFLOW_ID_CALCULATOR]
