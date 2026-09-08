from typing import Annotated, Any

from bson import ObjectId
from pydantic import BeforeValidator, WithJsonSchema


def validate_object_id(v: Any) -> str:
    """验证并转换 ObjectId。"""
    try:
        str_value = str(v) if not isinstance(v, str) else v
        ObjectId(str_value)
        return str_value
    except Exception as exc:
        raise ValueError("Not a valid ObjectId") from exc


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
