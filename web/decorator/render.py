# -*- coding: utf-8 -*-
# @File    : render.py
# @AUTH    : swxs
# @Time    : 2019/9/20 15:05

import logging
import asyncio
import functools
import urllib.parse
import collections
from web.result import SuccessData, ExceptionData, ResultData
from web.exceptions import ApiException, ApiUnknowException, Info

logger = logging.getLogger("main.web.render")


def render(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            result_data = func(self, *args, **kwargs)
            if isinstance(result_data, collections.Awaitable):
                result_data = await result_data
        except ApiException as ae:
            logger.exception(self.request.body)
            result_data = ExceptionData(ae)
        except Exception as e:
            ae = ApiUnknowException(e, Info.Base)
            logger.exception(self.request.body)
            result_data = ExceptionData(ae)
        finally:
            if isinstance(result_data, ResultData):
                return_type = self.request.headers.get("Content-Type", "application/json")
                if return_type.startswith("application/json"):
                    self.write_json(result_data.to_json(), status=200)
                self.finish()
            else:
                return result_data

    return wrapper


def render_file(func):
    content_type_dict = {
        'pdf': 'application/pdf',
        'png': 'image/png',
        'ppt': 'application/vnd.ms-powerpoint',
        'txt': 'text/plain',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.ms-excel',
        'gif': 'image/gif',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
    }

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        errors = None
        data = None
        file_name = None
        try:
            result_data = func(self, *args, **kwargs)
            if isinstance(result_data, collections.Awaitable):
                result_data = await result_data

            if isinstance(result_data, tuple) and len(result_data) > 1:
                file_name = result_data[0]
                data = result_data[1]
            else:
                file_name = 'index'
                for part in reversed(self.request.uri.split('/')):
                    if part:
                        file_name = part
                        break
                data = result_data
        except ApiException as ae:
            logger.exception(self.request.body)
            errors = ExceptionData(ae).to_json()
        except (Exception, NotImplementedError) as e:
            ae = ApiUnknowException(e, Info.Base)
            logger.exception(self.request.body)
            errors = ExceptionData(ae).to_json()
        finally:
            if errors is not None:
                self.set_header("Content-Type", "application/json; charset=UTF-8")
                self.write(errors)
            else:
                parts = file_name.split('.')
                suffix = parts[-1] if len(parts) > 1 else None
                content_type = content_type_dict.get(suffix, 'application/octet-stream')
                self.set_header('Content-Type', f'{content_type};content-type=utf-8')
                file_name = urllib.parse.quote(file_name)
                self.set_header('Content-Disposition', f'attachment;filename={file_name}')
                self.write(data)

    return wrapper


def render_thrift(result_thrift):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result_data = func(*args, **kwargs)
                if isinstance(result_data, collections.Awaitable):
                    result_data = await result_data
            except ApiException as ae:
                result_data = ExceptionData(ae)
            except Exception as e:
                ae = ApiUnknowException(e, Info.Base)
                result_data = ExceptionData(ae)
            return result_data

        return wrapper

    return decorator
