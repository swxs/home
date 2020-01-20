# -*- coding: utf-8 -*-

from apps.BaseConsts import HTTP_STATUS
from common.ApiExceptions.ApiException import ApiException


class ApiPermissionException(ApiException):
    '''
        权限错误
    '''

    def __init__(self, data=None):
        super(ApiPermissionException, self).__init__(code=HTTP_STATUS.AJAX_FAIL_AUTH, message=f"权限错误", data=data)
