# -*- coding: utf-8 -*-
# @File    : ApiReturnFileException.py
# @AUTH    : swxs
# @Time    : 2018/9/21 17:07

from apps.BaseConsts import HTTP_STATUS
from common.ApiExceptions.ApiException import ApiException


class ApiReturnFileException(ApiException):
    def __init__(self, filepath=None):
        super(ApiReturnFileException, self).__init__(code=HTTP_STATUS.AJAX_SUCCESS)
        self.filepath = filepath
