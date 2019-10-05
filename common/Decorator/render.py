# -*- coding: utf-8 -*-
# @File    : render.py
# @AUTH    : swxs
# @Time    : 2019/9/20 15:05

import asyncio
import functools
import urllib.parse
import collections
from result import SuccessData, ExceptionData, ResultData
from common.Exceptions import ApiException, ApiCommonException
from common.Utils.log_utils import getLogger

log = getLogger("views.render")


def render(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        result_data = None
        try:
            result_data = func(self, *args, **kwargs)
            if isinstance(result_data, collections.Awaitable):
                result_data = await result_data
        except ApiException as e:
            log.exception(self.request.body)
            result_data = ExceptionData(e)
        except (Exception, NotImplementedError) as e:
            log.exception(self.request.body)
            result_data = ExceptionData(ApiCommonException())
        finally:
            return_type = self.request.headers.get("Content-Type", "application/json")
            if return_type.startswith("application/json"):
                self.write_json(result_data.to_json(), status=200)
            self.finish()

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
            if isinstance(result_data, asyncio.Future):
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
        except ApiException as e:
            log.exception(self.request.body)
            errors = ExceptionData(e).to_json()
        except (Exception, NotImplementedError) as e:
            log.exception(self.request.body)
            errors = ExceptionData(ApiCommonException()).to_json()
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
