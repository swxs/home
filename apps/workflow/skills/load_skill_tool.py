# -*- coding: utf-8 -*-
"""
load_skill Tool：按名称加载技能说明文档，供 LLM 懒加载技能正文。
"""

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from apps.workflow.services.skill_loader import SKILL_LOADER


class LoadSkillTool(BaseTool):
    """按名称加载技能说明；不熟悉某技能时可先调用此工具获取完整说明。"""

    name: str = "load_skill"
    description: str = "按名称加载技能说明文档。不熟悉某技能时可先调用此工具获取完整说明，再根据说明处理用户问题。"

    class ArgsSchema(BaseModel):
        name: str = Field(description="技能名称，如 calculator")

    args_schema: type[BaseModel] = ArgsSchema

    def _run(self, name: str) -> str:
        return SKILL_LOADER.get_content(name)
