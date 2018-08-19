# -*- coding: utf-8 -*-

import json
import uuid
import binascii
import datetime
import functools
import traceback
import tornado.web
import tornado.escape
from tornado import locale, concurrent
from tornado.web import escape
import settings
from pycket.session import SessionMixin
from api.consts import const
from api.utils.user import User
from common.Exceptions import *
from common.Utils.validate import Validate, RegType
from common.Utils.log_utils import getLogger

log = getLogger()


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def prepare(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        log.debug('{} - {}:[{}]{} start'.format(now, self.request.remote_ip, self.request.method, self.request.uri))

    def on_finish(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        log.debug('{} - {}:[{}]{} finished'.format(now, self.request.remote_ip, self.request.method, self.request.uri))

    def _is_normal_argumnet(self):
        if not hasattr(self, "__normal_argumnet"):
            self.__normal_argumnet = (self.request.method.upper() == const.HTTP_METHOD_GET
                                      or Validate.has(str(self.request.headers), reg_type=RegType.FORM_GET))
        return self.__normal_argumnet

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
            except:
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
            except:
                value = []
            if value is None or value == []:
                return default
            return value

    def get_argument_file(self, argument, default=None, strip=True):
        if self.request.files:
            file = self.request.files[argument][0]
            return file
        else:
            return default

    def write_json(self, data=None, errcode=0, errmsg=None, status=None):
        ''''''
        self.set_header('Content-Type', 'text/json')
        if isinstance(status, int):
            self.set_status(status)
        dic = {'errcode': errcode, 'data': data or []}
        if errmsg:
            dic['errmsg'] = errmsg
        self.write(json.dumps(dic))

    def _handle_request_exception(self, e):
        if isinstance(e, ApiReturnException):
            self.write_json(data=e.data, errcode=e.code, errmsg=None, status=None)
            self.finish()
        elif isinstance(e, ApiException):
            self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            self.finish()
        else:
            try:
                log.error(traceback.format_exc()).split('\n')
            except ApiNotLoginException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
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
        ''''''
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
        ''''''
        if not hasattr(self, '_user'):
            user_id = self.session.get('user_id')
            if user_id is None:
                raise ApiNotLoginException()
            self._user = User.select(id=user_id)
        return self._user

    def get_user_locale(self):
        ''''''
        return self.locale

    def my_render(self, template, argus=None, rubbish_keys=None):
        ''''''
        if not isinstance(argus, dict):
            argus = dict()

        argus['xsrf_token'] = self.xsrf_token
        argus['is_ajax'] = self.is_ajax
        argus['locale'] = self.locale

        self.render(template, **argus)

    def xsrf_form_html(self):
        ''''''
        xsrf_key = settings.XSRF
        xsrf_val = escape.xhtml_escape(self.xsrf_token)
        t = '<input type="hidden" id="{0}" name="{0}" value="{1}"/>'
        return t.format(xsrf_key, xsrf_val)

    @property
    def xsrf_token(self):
        ''''''
        if not hasattr(self, "_xsrf_token"):
            token = self.get_cookie(settings.XSRF)
            if not token:
                token = binascii.b2a_hex(uuid.uuid4().bytes)
                exp = 30 if self.current_user else None
                self.set_cookie(settings.XSRF, token, expires_days=exp)
            self._xsrf_token = token
        return self._xsrf_token

    @property
    def is_ajax(self):
        ''''''
        if not hasattr(self, '_is_ajax'):
            self._is_ajax = self.request.headers.get('X-Requested-With')
        return self._is_ajax

    @property
    def locale(self):
        ''''''
        if not hasattr(self, '_locale'):
            local_code = self.get_cookie('locale')
            if not local_code:
                local_code = "zh_CN"
                self.set_cookie('local', local_code)
            self._locale = locale.get(local_code)
        return self._locale

    @classmethod
    def ajax_base(cls, method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            try:
                result = method(self, *args, **kwargs)
                if isinstance(result, concurrent.Future):
                    return result
                else:
                    self.write_json(data=result, errcode=const.AJAX_SUCCESS, errmsg=None, status=None)
            except ApiReturnException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=None, status=None)
                self.finish()
            except ApiException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except (Exception, NotImplementedError) as e:
                log.error(traceback.format_exc()).split('\n')
                self.write_json(data=None, errcode=const.AJAX_FAIL_NORMAL, errmsg=const.AJAX_FAIL_NORMAL, status=None)
            self.finish()

        return wrapper


class CsrfExceptMixin():
    def check_xsrf_cookie(self):
        return True
