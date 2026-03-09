# -*- coding: utf-8 -*-
"""
方式 B 扩展点：从 DB 或 YAML/JSON 配置加载工作流定义并动态构建 StateGraph。
二期实现：解析 config（节点类型、边、LLM 配置等），调用 LangGraph API 构建图并 compile()。
"""

from typing import Any, Dict


def build_graph_from_config(config: Dict[str, Any]):
    """
    根据配置字典动态构建 LangGraph 图。
    config 示例结构（二期）：{"nodes": [...], "edges": [...], "state_schema": ...}
    当前未实现，抛出 NotImplementedError。
    """
    raise NotImplementedError(
        "Config-driven workflow (方式 B) is not implemented yet. Use pre-registered workflow_id (e.g. 'echo') for now."
    )
