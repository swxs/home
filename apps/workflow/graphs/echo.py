# -*- coding: utf-8 -*-
"""
最小示例工作流：单节点，将输入 text 原样写入 output（无需 LLM）。
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class EchoState(TypedDict):
    """Echo 工作流状态：输入与输出均为字符串。"""

    text: str
    output: str


def echo_node(state: EchoState) -> dict:
    """单节点：把 text 拷贝到 output。"""
    return {"output": state.get("text", "")}


def build_echo_graph():
    """构建并编译 Echo 图（单节点）。"""
    graph = StateGraph(EchoState)
    graph.add_node("echo", echo_node)
    graph.add_edge(START, "echo")
    graph.add_edge("echo", END)
    return graph.compile()
