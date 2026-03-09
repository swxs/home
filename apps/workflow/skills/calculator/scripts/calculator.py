# -*- coding: utf-8 -*-
"""
计算器 Skill：对数学表达式进行安全求值，仅支持加减乘除与括号。
提供纯函数 calculate 与 LangChain Tool calculator_tool，供 LLM 绑定后按需调用。
"""

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


def calculate(expression: str) -> str:
    """
    安全求值数学表达式，仅允许数字与 + - * / ( )。
    非法或无法求值时返回错误信息字符串。
    """
    if not expression or not expression.strip():
        return "计算失败：表达式为空"
    expr = expression.strip()
    allowed = set("0123456789+-*/(). ")
    if not all(c in allowed for c in expr):
        return "计算失败：表达式仅支持数字与 + - * / ( )"
    try:
        result = eval(expr, {"__builtins__": None}, {})
        if isinstance(result, (int, float)):
            return f"计算结果：{result}"
        return f"计算结果：{result}"
    except Exception as e:
        return f"计算失败：{e!s}"


class CalculatorSkill(BaseTool):
    """计算器 Skill：供 LLM 通过 name/description 发现并决定是否调用。"""

    name: str = "calculator"
    description: str = (
        "用于数学计算，输入表达式字符串，返回计算结果。当用户问算式、数值计算、加减乘除时使用，如 (100+50)*3、10+20*2。"
    )

    class ArgsSchema(BaseModel):
        expression: str = Field(description="数学表达式，仅支持加减乘除与括号，如 5*(10+20)")

    args_schema: type[BaseModel] = ArgsSchema

    def _run(self, expression: str) -> str:
        return calculate(expression)
