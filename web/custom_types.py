from typing import Any, Generator

from bson import ObjectId


class OID(str):
    @classmethod
    def __get_validators__(cls) -> Generator:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        try:
            return ObjectId(str(v))
        except Exception:
            raise ValueError("Not a valid ObjectId")
