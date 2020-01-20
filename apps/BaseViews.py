# -*- coding: utf-8 -*-

import json
import os
import uuid
import binascii
import datetime
import functools
import traceback
from urllib.parse import quote
import tornado.web
import tornado.escape
from tornado import locale, concurrent
from tornado.web import escape
import settings
from common.Decorator.render import render
from common.Helpers.Helper_JWT import AuthCenter
from common.Helpers.Helper_validate import Validate, RegType
from common.Utils.pycket.session import SessionMixin
from common.Utils.log_utils import getLogger
from result import ExceptionData, ResultData

log = getLogger("views.Base")


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

    def _get_argument_as_dict(self):
        if not hasattr(self, "__dict_args"):
            self.__dict_args = json.loads(self.request.body)
        return self.__dict_args

    def get_argument(self, argument, default=None, strip=True):
        if self._is_normal_argumnet():
            return super(BaseHandler, self).get_argument(argument, default=default, strip=strip)
        else:
            try:
                value = self._get_argument_as_dict().get(argument, default)
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
                value = self._get_argument_as_dict().get(argument)
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

    def write_json(self, data, status=200):
        self.set_header('Content-Type', 'text/json')
        if isinstance(status, int):
            self.set_status(status)
        self.write(data)

    def _handle_request_exception(self, e):
        if isinstance(e, ApiException):
            self.write_json(ExceptionData(e).to_json(), status=200)
            self.finish()
        else:
            try:
                log.exception()
            except ApiNotLoginException as e:
                self.write_json(ExceptionData(e).to_json(), status=e.status)
                self.finish()
            else:
                super(BaseHandler, self)._handle_request_exception(e)

    def write_error(self, status_code, **kwargs):
        if settings.DEBUG:
            self.set_header('Content-Type', 'text/plain')
            exc_str = traceback.format_exception(*kwargs.get("exc_info"))
            m_info = ''.join(exc_str)
            self.finish(m_info)
        else:
            if status_code == 500:
                exception_info = traceback.format_exception(
                    *kwargs.get("exc_info"))
                exception_info = ''.join(exception_info).replace(
                    "\n", "<br>").replace(' ', '&nbsp;')
                error_info = {
                    'url': self.request.full_url(),
                    'time': datetime.datetime.now(),
                    'ip': self.request.remote_ip,
                    'info': exception_info,
                    'ua': self.request.headers.get('User-Agent'),
                    'request-body': self.request.body,
                    'method': self.request.method,
                }
                self.render("500.html")
                return
            self.render("error.html", msg=status_code)

    def check_xsrf_cookie(self):
        token = self.get_cookie(settings.XSRF, None) or \
                self.get_argument(settings.XSRF, None) or \
                self.request.headers.get("X-Xsrftoken") or \
                self.request.headers.get("X-Csrftoken")

        if not token:
            msg = "'%s' argument missing from POST" % settings.XSRF
            raise tornado.web.HTTPError(403, msg)
        if self.xsrf_token != token:
            msg = "XSRF cookie does not match POST argument"
            # raise tornado.web.HTTPError(403, msg)

    @property
    def current_user(self):
        if not hasattr(self, '_user'):
            user_id = self.session.get('user_id')
            if user_id is None:
                raise ApiNotLoginException()
            self._user = None
        return self._user

    @current_user.setter
    def current_user(self, user_id=None):
        if not hasattr(self, '_user'):
            if user_id is not None:
                raise ApiNotLoginException()

    def get_user_locale(self):
        return self.locale

    @property
    def locale(self):
        if not hasattr(self, '_locale'):
            local_code = self.get_cookie('locale', default=settings.DEFAULT_LOCAL)
            self.set_cookie('locale', local_code, expires_days=30)
            self._locale = locale.get(local_code)
        return self._locale

    @locale.setter
    def locale(self, local_code):
        self.set_cookie('locale', local_code)
        self._locale = locale.get(local_code)

    def my_render(self, template, argus=None, rubbish_keys=None):
        if not isinstance(argus, dict):
            argus = dict()

        argus['xsrf_token'] = self.xsrf_token
        argus['is_ajax'] = self.is_ajax
        argus['locale'] = self.locale

        self.render(template, **argus)

    @property
    def is_ajax(self):
        if not hasattr(self, '_is_ajax'):
            self._is_ajax = self.request.headers.get('X-Requested-With')
        return self._is_ajax

    @property
    def xsrf_token(self):
        if not hasattr(self, "_xsrf_token"):
            token = self.get_cookie(settings.XSRF)
            if not token:
                token = binascii.b2a_hex(uuid.uuid4().bytes)
                exp = 30 if self.current_user else None
                self.set_cookie(settings.XSRF, token, expires_days=exp)
            self._xsrf_token = token
        return self._xsrf_token

    def xsrf_form_html(self):
        xsrf_key = settings.XSRF
        xsrf_val = escape.xhtml_escape(self.xsrf_token)
        t = '<input type="hidden" id="{0}" name="{0}" value="{1}"/>'
        return t.format(xsrf_key, xsrf_val)

    def set_default_headers(self):
        self._headers.add("version", "1")


class PageNotFoundHandler(BaseHandler):
    @render
    def head(self):
        raise ApiNotFoundException()

    @render
    def get(self):
        raise ApiNotFoundException()

    @render
    def post(self):
        raise ApiNotFoundException()

    @render
    def put(self):
        raise ApiNotFoundException()

    @render
    def patch(self):
        raise ApiNotFoundException()

    @render
    def delete(self):
        raise ApiNotFoundException()
