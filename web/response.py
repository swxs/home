import json
import typing
import logging
import datetime

from bson import ObjectId
from fastapi.responses import JSONResponse

from dao.BaseDocument import BaseDocument

# 本模块方法
from .exceptions.http_exception import BaseHttpException

logger = logging.getLogger("web.response")


def encoder(obj):
    if isinstance(obj, BaseDocument):
        return obj.to_dict()
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, bytes):
        return obj.decode("utf8")
    else:
        raise Exception("Not NotImplemented")


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return encoder(obj)
        except Exception:
            return super(ComplexEncoder, self).default(obj)


class CustomJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=ComplexEncoder,
        ).encode("utf-8")


def response(status_code, code, message, data=None):
    """
    简介
    ----------


    参数
    ----------
    status_code :

    code :

    message :

    data [可选]: 默认为 None


    返回
    ----------

    """
    return CustomJSONResponse(
        {
            "code": code,
            "message": message,
            "data": data,
        },
        status_code=status_code,
    )


def success(data=None, message=''):
    """
    简介
    ----------


    参数
    ----------
    data [可选]: 默认为 None

    message [可选]: 默认为 ''


    返回
    ----------

    """
    return response(200, 0, message, data)


def exception(exc):
    """
    简介
    ----------


    参数
    ----------
    exc :


    返回
    ----------

    """
    if isinstance(exc, BaseHttpException):
        return response(exc.status_code, exc.code, exc.message, exc.data)
    else:
        logger.exception(f"未知异常")
        return response(500, -1, exc.args[0], {})
