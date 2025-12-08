from typing import Annotated, Any

from bson import ObjectId
from pydantic import BeforeValidator, WithJsonSchema


def validate_object_id(v: Any) -> str:
    """
    验证并转换 ObjectId

    Args:
        v: 输入值（可以是字符串、ObjectId等）

    Returns:
        转换后的字符串格式的 ObjectId

    Raises:
        ValueError: 如果不是有效的 ObjectId
    """
    try:
        if not isinstance(v, str):
            str_value = str(v)
        else:
            str_value = v
        # 尝试转换为字符串再验证
        ObjectId(str_value)
        return str_value
    except Exception:
        raise ValueError("Not a valid ObjectId")


# 使用 Annotated 定义 objectId 类型，支持 Pydantic v2
# WithJsonSchema 用于生成 JSON Schema，避免 PlainValidatorFunctionSchema 错误
objectId = Annotated[
    str,
    BeforeValidator(validate_object_id),
    WithJsonSchema(
        {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{24}$",
            "description": "Like MongoDB ObjectId (24 character hex string)",
            "examples": ["507f1f77bcf86cd799439011"],
        },
    ),
]
