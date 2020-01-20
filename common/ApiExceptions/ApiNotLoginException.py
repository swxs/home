# -*- coding: utf-8 -*-

from apps.BaseConsts import HTTP_STATUS
from common.ApiExceptions.ApiException import ApiException


class ApiNotLoginException(ApiException):
    '''
        用户未登录
    '''

    def __init__(self):
        super(ApiNotLoginException, self).__init__(code=HTTP_STATUS.AJAX_FAIL_NOTLOGIN, message="用户未登录")
