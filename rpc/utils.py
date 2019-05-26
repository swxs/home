#!/usr/bin/python
import traceback
import types
from common.Exceptions import ApiException


def is_coroutine(func):
    """
    判断函数是否为协程函数

    :param func: 函数
    :return:
    """

    if func.__class__ is types.FunctionType and getattr(func, '__code__', None).__class__ is types.CodeType:
        co_flags = func.__code__.co_flags
        if co_flags & 0x180:
            return True
    return False


def render_thrift(result_cls):
    def decorator(func):

        async def wrapper_async(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ApiException as ae:
                data = ae.data
                err_obj = result_cls()
                err_obj.code = data.get('code')
                err_obj.msg = data.get('msg')
                if data.get('data'):
                    err_obj.data = data.get('data')
            except Exception:
                err_obj = result_cls()
                err_obj.code = -1
                err_obj.msg = 'Request handler no return value.'
                traceback.print_exc()
            return err_obj

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ApiException as ae:
                data = ae.data
                err_obj = result_cls()
                err_obj.code = data.get('code')
                err_obj.msg = data.get('msg')
                if data.get('data'):
                    err_obj.data = data.get('data')
            except Exception:
                err_obj = result_cls()
                err_obj.code = -1
                err_obj.msg = 'Request handler no return value.'
            return err_obj

        if is_coroutine(func):
            return wrapper_async
        else:
            return wrapper

    return decorator
