# -*- coding: utf-8 -*-

import json
import os
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
from web.decorator.render import render
from web.exceptions import ApiCommonException, CommmonExceptionInfo as ei
from web.result import ExceptionData, ResultData
from common.Helpers.Helper_validate import Validate, RegType
from common.Utils.pycket.session import SessionMixin
from common.Utils.log_utils import getLogger

log = getLogger("web")


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def prepare(self):
        log.info(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f} - {self.request.remote_ip}:[{self.request.method}]{self.request.uri} start')

    def on_finish(self):
        log.info(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S.%f} - {self.request.remote_ip}:[{self.request.method}]{self.request.uri} finished')

    def _is_normal_argumnet(self):
        if not hasattr(self, "__normal_argument"):
            self.__normal_argument = (
                self.request.method.upper() in ("GET", "DELETE")
                or Validate.has(str(self.request.headers), reg_type=RegType.FORM_GET)
                or Validate.has(str(self.request.headers), reg_type=RegType.FORM_FILE)
            )
        return self.__normal_argument

    @property
    def arguments(self):
        if not hasattr(self, "__arguments"):
            self.__arguments = json.loads(self.request.body)
        return self.__arguments

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
        if self.config.DEBUG:
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
            token = self.get_cookie(self.config.XSRF)
            if not token:
                token = binascii.b2a_hex(uuid.uuid4().bytes)
                exp = 30 if self.current_user else None
                self.set_cookie(self.config.XSRF, token, expires_days=exp)
            self._xsrf_token = token
        return self._xsrf_token

    def check_xsrf_cookie(self):
        token = self.get_cookie(self.config.XSRF, None) or \
                self.get_argument(self.config.XSRF, None) or \
                self.request.headers.get("X-Xsrftoken") or \
                self.request.headers.get("X-Csrftoken")

        if not token:
            msg = "'%s' argument missing from POST" % self.config.XSRF
            raise tornado.web.HTTPError(403, msg)
        if self.xsrf_token != token:
            msg = "XSRF cookie does not match POST argument"
            # raise tornado.web.HTTPError(403, msg)

    def xsrf_form_html(self):
        xsrf_key = self.config.XSRF
        xsrf_val = escape.xhtml_escape(self.xsrf_token)
        t = '<input type="hidden" id="{0}" name="{0}" value="{1}"/>'
        return t.format(xsrf_key, xsrf_val)


class PageNotFoundHandler(BaseHandler):
    @render
    def head(self):
        raise ApiCommonException(ei.PageNotFoundException)

    @render
    def get(self):
        raise ApiCommonException(ei.PageNotFoundException)

    @render
    def post(self):
        raise ApiCommonException(ei.PageNotFoundException)

    @render
    def put(self):
        raise ApiCommonException(ei.PageNotFoundException)

    @render
    def patch(self):
        raise ApiCommonException(ei.PageNotFoundException)

    @render
    def delete(self):
        raise ApiCommonException(ei.PageNotFoundException)


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
            module = path.replace('\\', '/').replace(
                root.replace('\\', '/'), '')
            if module.startswith('/'):
                module = module[1:]
            module = module.replace('.py', '').replace('.PY', '')
            if set('.#~') & set(module):
                return None
            module = module.replace('/', '.').strip()
            if module:
                return module
        return None