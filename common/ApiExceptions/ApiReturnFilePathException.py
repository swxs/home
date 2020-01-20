# -*- coding: utf-8 -*-
# @File    : ApiReturnFilePathException.py
# @AUTH    : swxs
# @Time    : 2018/9/25 17:58

import os
from apps.BaseConsts import HTTP_STATUS
from common.ApiExceptions.ApiException import ApiException


class ApiReturnFilePathException(ApiException):
    def __init__(self, filepath=None):
        super(ApiReturnFilePathException, self).__init__(code=HTTP_STATUS.AJAX_SUCCESS)
        self.path, self.filename = os.path.split(filepath)
        self.data = {"filename": self.filename}
