# -*- coding: utf-8 -*-
"""
计算器工作流（仅 load_skill）：LLM 只能调用 load_skill 按需加载技能说明；
calculator 仅作为 SKILL.md 文档存在，无独立 calculator tool。
"""

import operator
from typing import Annotated, Any, Dict, List, TypedDict

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import SecretStr

import core.config

from apps.workflow.services.skill_loader import SKILL_LOADER
from apps.workflow.skills.load_skill_tool import LoadSkillTool


class AgentState(TypedDict):
    """Agent 状态：用户问题、消息历史、工具调用结果、最终回答。"""

    query: str
    messages: Annotated[List[BaseMessage], operator.add]
    tool_results: List[Dict[str, Any]]
    answer: str


def _get_llm():
    """与 summarize 一致的 LLM 配置。"""
    return ChatOpenAI(
        api_key=SecretStr(core.config.WORKFLOW_OPENAI_API_KEY),
        base_url=core.config.WORKFLOW_OPENAI_BASE_URL,
        model=core.config.WORKFLOW_DEFAULT_MODEL,
    )


def _get_system_content() -> str:
    """注入可用技能列表，说明使用 load_skill 可获取完整说明。"""
    descriptions = SKILL_LOADER.get_descriptions()
    return (
        "你是计算器助手。可用技能列表（仅名称与简短描述）：\n"
        f"{descriptions}\n"
        "使用 load_skill 工具可获取某技能的完整说明，再根据说明回答用户。"
    )


def _get_llm_with_tools():
    return _get_llm().bind_tools([LoadSkillTool()])


def llm_node(state: AgentState) -> Dict[str, Any]:
    """模型决策节点：根据 messages 生成回复或调用 load_skill。"""
    messages = state.get("messages", [])
    system_msg = SystemMessage(content=_get_system_content())
    input_messages = [system_msg] + list(messages)
    llm = _get_llm_with_tools()
    response = llm.invoke(input_messages)
    return {"messages": [response]}


def skill_executor_node(state: AgentState) -> Dict[str, Any]:
    """仅处理 load_skill：返回 SKILL 正文并写回 ToolMessage。"""
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage) or not getattr(last_message, "tool_calls", None):
        return {"tool_results": []}
    tool_calls = last_message.tool_calls
    new_messages = []
    for tc in tool_calls:
        name = tc.get("name", "")
        args = tc.get("args", {}) or {}
        tid = tc.get("id", "")
        if name == "load_skill":
            skill_name = args.get("name", "")
            content = SKILL_LOADER.get_content(skill_name)
            new_messages.append(ToolMessage(content=content, tool_call_id=tid))
    return {"messages": new_messages, "tool_results": []}


def answer_node(state: AgentState) -> Dict[str, Any]:
    """结果整合节点：若有工具调用则用 LLM 整合结果生成回答，否则用模型直接回复作为 answer。"""
    tool_results = state.get("tool_results") or []
    messages = state.get("messages", [])
    query = state.get("query", "")

    if tool_results:
        prompt = (
            f"基于以下信息，用简洁自然的中文回答用户问题：{query}\n\n"
            f"工具调用结果：{tool_results}\n\n"
            "要求：准确引用结果中的关键信息，语言流畅。"
        )
        llm = _get_llm()
        msg = llm.invoke([HumanMessage(content=prompt)])
        answer = msg.content if hasattr(msg, "content") else str(msg)
    else:
        # 未调用工具时，最后一条约是模型的直接回复
        answer = ""
        for m in reversed(messages):
            if isinstance(m, AIMessage) and m.content:
                answer = m.content if isinstance(m.content, str) else str(m.content)
                break
    return {"answer": answer or "（无回复）"}


def _should_call_skill(state: AgentState) -> str:
    """条件边：模型是否请求调用 Skill。"""
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "skill_executor_node"
    return "answer_node"


def build_calculator_graph():
    """构建并编译 Skills 型计算器 Agent 图。"""
    graph = StateGraph(AgentState)
    graph.add_node("llm_node", llm_node)
    graph.add_node("skill_executor_node", skill_executor_node)
    graph.add_node("answer_node", answer_node)
    graph.add_edge(START, "llm_node")
    graph.add_conditional_edges("llm_node", _should_call_skill)
    graph.add_edge("skill_executor_node", "llm_node")
    graph.add_edge("answer_node", END)
    return graph.compile()
