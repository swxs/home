# -*- coding: utf-8 -*-

import asyncio
from typing import Any, Dict

import core.config

from apps.workflow.graphs import get_graph


async def run_workflow(workflow_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    在线程池中同步执行 LangGraph，避免阻塞事件循环。
    返回图执行后的最终 state（作为 output）。
    """
    graph = get_graph(workflow_id)
    timeout = getattr(core.config, "WORKFLOW_RUN_TIMEOUT_SECONDS", 60)
    loop = asyncio.get_event_loop()
    result = await asyncio.wait_for(
        loop.run_in_executor(None, lambda: graph.invoke(inputs)),
        timeout=float(timeout),
    )
    return dict(result) if hasattr(result, "keys") else {"result": result}
