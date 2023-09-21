from fastapi import Request

# 本模块方法
from ..exceptions.http_404_not_found_exception import Http404NotFoundException
from ..response import exception


async def unknown_http_handler(_: Request, exc: Exception):
    """
    http异常处理
    :param _:
    :param exc:
    :return:
    """

    return exception(Http404NotFoundException(Http404NotFoundException.MethodNotFoundError, "方法不存在"))
