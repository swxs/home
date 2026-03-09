# -*- coding: utf-8 -*-
"""
文本总结工作流：单节点，通过 LLM + Prompt 总结输入文本的关键信息。
"""

from typing import TypedDict

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import SecretStr

import core.config


class SummarizeState(TypedDict):
    """文本总结工作流状态：输入文本与输出总结。"""

    text: str
    summary: str


def summarize_node(state: SummarizeState) -> dict:
    """单节点：使用 LLM 总结 state["text"]，写入 summary。"""
    llm = ChatOpenAI(
        api_key=SecretStr(core.config.WORKFLOW_OPENAI_API_KEY),
        base_url=core.config.WORKFLOW_OPENAI_BASE_URL,
        model=core.config.WORKFLOW_DEFAULT_MODEL,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("user", "请总结以下文本的关键信息：\n\n{text}"),
        ]
    )
    chain = prompt | llm
    message = chain.invoke({"text": state.get("text", "")})
    summary = message.content if hasattr(message, "content") else str(message)
    return {"summary": summary}


def build_summarize_graph():
    """构建并编译文本总结图（单节点）。"""
    graph = StateGraph(SummarizeState)
    graph.add_node("summarize", summarize_node)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", END)
    return graph.compile()
