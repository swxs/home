# -*- coding: utf-8 -*-

import json
import uuid
import binascii
import datetime
import functools
import traceback
from pycket.session import SessionMixin
import tornado.web
import tornado.escape
from tornado import locale
from tornado.web import escape

import const
import settings
from common.Exceptions.CommonException import CommonException
from common.Exceptions.ExistException import ExistException
from common.Exceptions.NotExistException import NotExistException
from common.Exceptions.NotLoginException import NotLoginException
from common.Exceptions.PermException import PermException
from common.Exceptions.ValidateException import ValidateException
from common.Exceptions.LackOfFieldException import LackOfFieldException
from common.Exceptions.DeleteInhibitException import DeleteInhibitException
from common.Utils.validate import Validate


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def prepare(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print '{} - {}:{} start'.format(now, self.request.remote_ip, self.request.uri)

    def on_finish(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print '{} - {}:{} finished'.format(now, self.request.remote_ip, self.request.uri)

    def get_argument(self, argument, default=None, strip=True):
        if self.request.method == "GET" or Validate.has(str(self.request.headers), reg_type="json_header"):
            return super(BaseHandler, self).get_argument(argument, default=default, strip=strip)
        else:
            try:
                arguments = json.loads(self.request.body)
                value = arguments.get(argument)
            except:
                value = None
            if value is None:
                return default
            return value

    def get_arguments(self, argument, default=None, strip=True):
        if self.request.method == "GET" or Validate.has(str(self.request.headers), reg_type="json_header"):
            value = super(BaseHandler, self).get_arguments(argument, strip=True)
            if value == []:
                return default
            return value
        else:
            try:
                arguments = json.loads(self.request.body)
                value = arguments.get(argument)
            except:
                value = None
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

    def get_current_user(self):
        ''''''
        return None
        # if not hasattr(self, '_user'):
        #     user_id = self.session.get('user_id')
        #     if user_id is None:
        #         raise NotLoginException()
        #     self._user = user_utils.get_user(user_id=user_id)
        # return self._user

    def get_template_namespace(self):
        namespace = super(BaseHandler, self).get_template_namespace()
        namespace['escape'] = tornado.escape
        namespace['json'] = json
        # namespace['common_utils'] = common_utils
        namespace['has_permission'] = self.has_permission
        namespace['const'] = const
        return namespace

    def get_rubbish_key(self, rubbish_keys):
        ''''''
        result = set(['self'])
        if hasattr(rubbish_keys, '__iter__'):
            for key in rubbish_keys:
                result.add(key)
        return result

    def get_user_locale(self):
        ''''''
        return self.locale

    def my_render(self, template, argus=None, rubbish_keys=None):
        ''''''
        if not isinstance(argus, dict):
            argus = {}
        else:
            for key in self.get_rubbish_key(rubbish_keys):
                if key in argus:
                    del argus[key]

        argus['xsrf_token'] = self.xsrf_token
        argus['is_mobile'] = self.is_mobile
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
    def is_mobile(self):
        ''''''
        if hasattr(self, '_client_type'):
            return getattr(self, '_client_type')

        agent = self.request.headers.get('USER-AGENT', '')
        return False
        # is_mobile = is_mobile_request(agent)

        # setattr(self, '_client_type', is_mobile)
        # return is_mobile

    @property
    def is_ajax(self):
        ''''''
        if not hasattr(self, '_is_ajax'):
            if self.request.headers.get('X-Requested-With'):
                self._is_ajax = const.yes_or_no['yes']
            else:
                self._is_ajax = 0
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
        ''''''
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            ''''''
            try:
                data = method(self, *args, **kwargs)
                self.write_json(data=data, errcode=const.AJAX_SUCCESS, errmsg=None, status=None)
            except CommonException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except ValidateException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except ExistException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except NotExistException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except PermException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except NotLoginException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except LackOfFieldException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except DeleteInhibitException as e:
                self.write_json(data=e.data, errcode=e.code, errmsg=e.message, status=None)
            except Exception as e:
                from common.Utils.log_utils import getLogger
                import traceback
                log = getLogger()
                log.error(e)
                self.write_json(data=None, errcode=const.AJAX_FAIL_NORMAL,
                                errmsg=u"未定义异常", status=None)

        return wrapper


class CsrfExceptMixin():
    def check_xsrf_cookie(self):
        return True


class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("error.html", msg="page not found")

    def post(self):
        self.render("error.html", msg="page not found")

    def initialize(self, status_code):
        self.set_status(status_code)
