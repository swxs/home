# -*- coding: utf-8 -*-

import json
import os
from re import template
import uuid
import binascii
import datetime
import functools
import traceback
import tornado.web
import tornado.escape
from urllib.parse import quote
from importlib import import_module
from tornado import locale, concurrent
from tornado.web import url, escape, Application

import settings
from web.decorator.render import render
from web.exceptions import ApiException, ApiUnknowException, Info
from web.result import ExceptionData, ResultData
from common.Helpers.Helper_JWT import AuthTokner, InvalidSignatureError, ExpiredSignatureError, ImmatureSignatureError
from common.Helpers.Helper_validate import Validate, RegType
from common.Utils.pycket.session import SessionMixin
from common.Utils.log_utils import getLogger

log = getLogger("web")

tokener = AuthTokner(key=settings.JWT_SECRET_KEY, timeout=settings.JWT_TIMEOUT)
refresh_tokener = AuthTokner(key=settings.JWT_SECRET_KEY, timeout=settings.JWT_REFRESH_TIMEOUT)


class BaseHandler(tornado.web.RequestHandler):
    """
    简介
    ----------
    句柄基类
    记录每个接口的调用信息
    提供一些获取参数的方法
    """

    def prepare(self):
        log.info(
            f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f} - {self.request.remote_ip}:[{self.request.method}]{self.request.uri} start'
        )

    def on_finish(self):
        log.info(
            f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f} - {self.request.remote_ip}:[{self.request.method}]{self.request.uri} finished'
        )

    @render
    async def _unimplemented_method(self, *args: str, **kwargs: str) -> None:
        raise ApiException(Info.PageNotFound)

    head = _unimplemented_method
    get = _unimplemented_method
    post = _unimplemented_method
    delete = _unimplemented_method
    patch = _unimplemented_method
    put = _unimplemented_method
    options = _unimplemented_method

    def _is_normal_argumnet(self):
        if not hasattr(self, "_normal_argument"):
            self._normal_argument = (
                (self.request.method.upper() in ("GET", "DELETE"))
                or (Validate.has(str(self.request.headers), reg_type=RegType.FORM_GET))
                or (Validate.has(str(self.request.headers), reg_type=RegType.FORM_FILE))
            )
        return self._normal_argument

    @property
    def arguments(self):
        if not hasattr(self, "_arguments"):
            self._arguments = {}
            for key, value in self.request.query_arguments.items():
                self._arguments[key] = value[0].decode('utf8')
            self._arguments.update(self.request.body_arguments)
            if self.request.body:
                self._arguments.update(json.loads(self.request.body))
        return self._arguments

    def get_argument(self, argument, default=None, strip=True):
        if self._is_normal_argumnet():
            return super(BaseHandler, self).get_argument(argument, default=default, strip=strip)
        else:
            try:
                value = self.arguments.get(argument, default)
                if strip:
                    try:
                        value = value.strip()
                    except Exception:
                        pass
            except Exception:
                value = default
            return value

    def get_arguments(self, argument, default=None, strip=True):
        if self._is_normal_argumnet():
            value = super(BaseHandler, self).get_arguments(argument, strip=True)
            if value == []:
                return default
            return value
        else:
            try:
                value = self.arguments.get(argument)
            except Exception:
                value = []
            if value is None:
                return default
            return value

    def get_argument_file(self, argument, default=None, strip=True):
        if self.request.files:
            file = self.request.files[argument][0]
            return file
        else:
            return default

    @property
    def locale(self):
        if not hasattr(self, '__locale'):
            local_code = self.get_cookie('locale', default=self.config.DEFAULT_LOCAL)
            self.set_cookie('locale', local_code, expires_days=30)
            self._locale = locale.get(local_code)
        return self._locale

    @locale.setter
    def locale(self, local_code):
        self.set_cookie('locale', local_code)
        self.__locale = locale.get(local_code)

    def write_json(self, data, status=200):
        self.set_header('Content-Type', 'text/json')
        if isinstance(status, int):
            self.set_status(status)
        self.write(data)

    def write_error(self, status_code, **kwargs):
        if self.settings.DEBUG:
            self.set_header('Content-Type', 'text/plain')
            self.finish('\n'.join(traceback.format_exception(*kwargs.get("exc_info"))))
        else:
            self.finish('')

    @property
    def is_ajax(self):
        if not hasattr(self, '_is_ajax'):
            self._is_ajax = self.request.headers.get('X-Requested-With')
        return self._is_ajax

    @property
    def xsrf_token(self):
        if not hasattr(self, "_xsrf_token"):
            token = self.get_cookie(self.settings.XSRF)
            if not token:
                token = binascii.b2a_hex(uuid.uuid4().bytes)
                exp = 30 if self.current_user else None
                self.set_cookie(self.settings.XSRF, token, expires_days=exp)
            self._xsrf_token = token
        return self._xsrf_token

    def check_xsrf_cookie(self):
        token = (
            self.get_cookie(self.settings.XSRF, None)
            or self.get_argument(self.settings.XSRF, None)
            or self.request.headers.get("X-Xsrftoken")
            or self.request.headers.get("X-Csrftoken")
        )

        if not token:
            msg = "'%s' argument missing from POST" % self.settings.XSRF
            raise tornado.web.HTTPError(403, msg)
        if self.xsrf_token != token:
            msg = "XSRF cookie does not match POST argument"
            # raise tornado.web.HTTPError(403, msg)

    def xsrf_form_html(self):
        xsrf_key = self.settings.XSRF
        xsrf_val = escape.xhtml_escape(self.xsrf_token)
        t = '<input type="hidden" id="{0}" name="{0}" value="{1}"/>'
        return t.format(xsrf_key, xsrf_val)


class BaseAuthedHanlder(BaseHandler):
    """
    简介
    ----------
    需要校验权限的句柄类
    提供一些从状态信息中获取数据的方法
    """

    def __init__(self, *args, **kwargs):
        self.__token_header = {}
        self.__token_payload = {}
        super(BaseAuthedHanlder, self).__init__(*args, **kwargs)

    async def prepare(self):
        super(BaseAuthedHanlder, self).prepare()
        await self.check_jwt_token()

    def __get_request_token(self):
        headers = self.request.headers
        if headers:
            authorization: str = headers.get('Authorization')
            if not authorization:
                raise ApiException(Info.TokenLost, template='No "Authorization" in request headers.')
            if not authorization.lower().startswith('bearer'):
                raise ApiException(Info.TokenIllegal, template='"Bearer" not in "Authorization".')
            return authorization[authorization.rfind(' ') :].strip()
        return None

    @render
    async def check_jwt_token(self):
        self.request_token = self.__get_request_token()  # 形如：Authorization: Bearer <token>
        if not self.request_token:
            raise ApiException(Info.TokenLost, template='No token')

        try:
            header, payload = tokener.decode(self.request_token)
            if header:
                self.__token_header.update(header)
            if payload:
                self.__token_payload.update(payload)
        except InvalidSignatureError:
            raise ApiException(Info.TokenIllegal, template='Invalid Token.')
        except ExpiredSignatureError:
            raise ApiException(Info.TokenTimeout, template='Token expire date.')
        except ImmatureSignatureError:
            raise ApiException(Info.TokenIllegal, template='Immature signature.')
        except Exception as e:
            raise ApiUnknowException(e, Info.Base)

    @property
    def tokens(self):
        return self.__token_payload


class PageNotFoundHandler(BaseHandler):
    @render
    def head(self):
        raise ApiException(Info.PageNotFound)

    @render
    def get(self):
        raise ApiException(Info.PageNotFound)

    @render
    def post(self):
        raise ApiException(Info.PageNotFound)

    @render
    def put(self):
        raise ApiException(Info.PageNotFound)

    @render
    def patch(self):
        raise ApiException(Info.PageNotFound)

    @render
    def delete(self):
        raise ApiException(Info.PageNotFound)


class IBApplication(Application):
    def __init__(self, default_host=None, transforms=None, **settings):
        super(IBApplication, self).__init__(default_host=default_host, transforms=transforms, **settings)

    def register_handlers(self, path):
        base_handlers = []
        for root, dirs, files in os.walk(os.path.join(path, "apps")):
            for filename in files:
                if filename.endswith('.py') or filename.endswith('.PY'):
                    module = self._path_2_module(path=os.path.join(root, filename), root=path)
                    if module:
                        mod = import_module(module)
                        if hasattr(mod, 'URL_MAPPING_LIST'):
                            base_handlers.append(mod.URL_MAPPING_LIST)
        for handlers in base_handlers:
            self.add_handlers('.*$', handlers)
        self.add_handlers(".*$", [url(r".*", PageNotFoundHandler)])

    @staticmethod
    def _path_2_module(path='', root=''):
        if path:
            module = path.replace('\\', '/').replace(root.replace('\\', '/'), '')
            if module.startswith('/'):
                module = module[1:]
            module = module.replace('.py', '').replace('.PY', '')
            if set('.#~') & set(module):
                return None
            module = module.replace('/', '.').strip()
            if module:
                return module
        return None
