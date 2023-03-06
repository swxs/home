from fastapi import Request

# 本模块方法
from ..response import exception


async def unknown_exception_handler(_: Request, exc: Exception):
    """
    http异常处理
    :param _:
    :param exc:
    :return:
    """

    return exception(exc)
