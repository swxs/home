import os
import json
import typing
import logging
import datetime
from urllib.parse import quote

from bson import ObjectId
from fastapi.responses import JSONResponse, RedirectResponse, Response
from pydantic import BaseModel
from starlette.background import BackgroundTask
from starlette.types import Receive, Scope, Send

# 本模块方法
from .exceptions.http_exception import BaseHttpException

logger = logging.getLogger("main.web.response")


def encoder(obj):
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime.datetime):
        return obj.strftime("%Y/%m/%d %H:%M:%S")
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


def _add_cors_headers_to_response(response: Response) -> None:
    """为响应添加 CORS 头的内部函数"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    # 注意：当 Access-Control-Allow-Origin 为 * 时，不能设置 Access-Control-Allow-Credentials 为 true


class CORSResponse(Response):
    """自动包含 CORS 头的 Response 基类"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_cors_headers_to_response(self)


class CORSJSONResponse(JSONResponse):
    """自动包含 CORS 头的 JSONResponse"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_cors_headers_to_response(self)


class CORSRedirectResponse(RedirectResponse):
    """自动包含 CORS 头的 RedirectResponse"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_cors_headers_to_response(self)


class CORSCustomJSONResponse(CustomJSONResponse):
    """自动包含 CORS 头的 CustomJSONResponse"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_cors_headers_to_response(self)


class CustomFileresponse(Response):
    def __init__(
        self,
        data: bytes,
        status_code: int = 200,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
        filename: typing.Optional[str] = None,
        content_disposition_type: str = "attachment",
    ) -> None:
        self.data = data
        self.status_code = status_code
        self.filename = filename
        if media_type is None:
            media_type = "text/plain"
        self.media_type = media_type
        self.background = background
        self.init_headers(headers)
        if self.filename is not None:
            content_disposition_filename = quote(self.filename)
            if content_disposition_filename != self.filename:
                content_disposition = "{}; filename*=utf-8''{}".format(
                    content_disposition_type, content_disposition_filename
                )
            else:
                content_disposition = '{}; filename="{}"'.format(content_disposition_type, self.filename)
            self.headers.setdefault("content-disposition", content_disposition)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": self.data,
                "more_body": False,
            }
        )

        if self.background is not None:
            await self.background()


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


def success(data=None, message=""):
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
