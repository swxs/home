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
from common.Helpers.Helper_JWT import AuthCenter
from common.Utils.pycket.session import SessionMixin
from api.consts.const import HTTP_METHOD_GET, HTTP_METHOD_DELETE, HTTP_STATUS
from api.utils.user import User
from common.Exceptions import *
from common.Utils.validate import Validate, RegType
from common.Utils.log_utils import getLogger

log = getLogger()


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def prepare(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        log.info(f'{now} - {self.request.remote_ip}:[{self.request.method}]{self.request.uri} start')

    def on_finish(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        log.info(f'{now} - {self.request.remote_ip}:[{self.request.method}]{self.request.uri} finished')

    def _is_normal_argumnet(self):
        if not hasattr(self, "__normal_argumnet"):
            self.__normal_argumnet = (self.request.method.upper() in (HTTP_METHOD_GET, HTTP_METHOD_DELETE)
                                      or Validate.has(str(self.request.headers), reg_type=RegType.FORM_GET)
                                      or Validate.has(str(self.request.headers), reg_type=RegType.FORM_FILE))
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
                if strip:
                    try:
                        value = value.strip()
                    except:
                        pass
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
            if value is None:
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

    @current_user.setter
    def current_user(self, user_id=None):
        if not hasattr(self, '_user'):
            if user_id is not None:
                raise ApiNotLoginException()
            self._user = User.select(id=user_id)

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
    def access_token(self):
        if not hasattr(self, '_access_token'):
            self._access_token = self.request.headers.get('access_token')
        return self._access_token

    @access_token.setter
    def access_token(self, token):
        self._headers.add('access_token', token)

    @property
    def refresh_token(self):
        if not hasattr(self, '_refresh_token'):
            self._refresh_token = self.request.headers.get('refresh_token')
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, token):
        self._headers.add('refresh_token', token)

    @property
    def locale(self):
        ''''''
        if not hasattr(self, '_locale'):
            local_code = self.get_cookie('locale', default=settings.DEFAULT_LOCAL)
            self.set_cookie('locale', local_code, expires_days=30)
            self._locale = locale.get(local_code)
        return self._locale

    @locale.setter
    def locale(self, local_code):
        self.set_cookie('locale', local_code)
        self._locale = locale.get(local_code)

    def _do_filter(self, result, filter):
        if len(filter) == 1:
            if filter[0] in result:
                result.pop(filter[0])
            return result
        else:
            checked = result.get(filter[0])
            if isinstance(checked, dict):
                result[filter[0]] = self._do_filter(checked, filter[1:])
            elif isinstance(checked, list):
                result[filter[0]] = [self._do_filter(new_result, filter[1:]) for new_result in checked]
            return result

    def _filter_result(self, result):
        if isinstance(result, dict):
            filters = self.get_query_argument("filters", "").split("|")
            for filter in filters:
                f = filter.split(".")
                result = self._do_filter(result, f)
        return result

    @classmethod
    def ajax_base(cls, login=False, aio=False):

        def function(method):

            @functools.wraps(method)
            async def wrapper(self, *args, **kwargs):
                try:
                    if not login:
                        playload = AuthCenter.identify(self.access_token)
                        self.current_user_id = playload.get("id")
                    if aio:
                        result = await method(self, *args, **kwargs)
                    else:
                        result = method(self, *args, **kwargs)
                    if isinstance(result, concurrent.Future):
                        return result
                    else:
                        self.write_json(data=result, errcode=HTTP_STATUS.AJAX_SUCCESS)
                except ApiNotFoundException as e:
                    self.write_json(data=e.data, errcode=e.code)
                except ApiReturnException as e:
                    self.write_json(data=e.data, errcode=e.code)
                except ApiRedirectException as e:
                    return self.redirect(e.url)
                except ApiReturnFilePathException as e:
                    self.write_json(data=e.data, errcode=e.code)
                except ApiReturnFileException as e:
                    path, filename = os.path.split(e.filepath)
                    export_filename = f"filename={quote(filename)}"
                    name, ext = os.path.splitext(filename)
                    if ext in [".xlsx" ".xls"]:
                        self.set_header("Content-Type", "application/vnd.ms-excel")
                    self.set_header("Content-Type", "application/force-download")
                    self.set_header("Content-Disposition", f"attachment; {export_filename}")
                    with open(e.filepath, 'rb') as f:
                        buf_size = 4096
                        while 1:
                            data = f.read(buf_size)
                            if not data:
                                break
                            self.write(data)
                except ApiException as e:
                    self.write_json(data=e.data, errcode=e.code, errmsg=e.message)
                except (Exception, NotImplementedError) as e:
                    log.error(repr(e))
                    self.write_json(data=None, errcode=HTTP_STATUS.AJAX_FAIL_NORMAL)
                self.finish()

            return wrapper

        return function


class CsrfExceptMixin():
    def check_xsrf_cookie(self):
        return True


class PageNotFoundHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def head(self):
        raise ApiNotFoundException()

    @BaseHandler.ajax_base()
    def get(self):
        raise ApiNotFoundException()

    @BaseHandler.ajax_base()
    def post(self):
        raise ApiNotFoundException()

    @BaseHandler.ajax_base()
    def put(self):
        raise ApiNotFoundException()

    @BaseHandler.ajax_base()
    def patch(self):
        raise ApiNotFoundException()

    @BaseHandler.ajax_base()
    def delete(self):
        raise ApiNotFoundException()
