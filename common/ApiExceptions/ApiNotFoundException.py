from apps.BaseConsts import HTTP_STATUS
from common.ApiExceptions import ApiException


class ApiNotFoundException(ApiException):
    def __init__(self):
        super(ApiNotFoundException, self).__init__(code=HTTP_STATUS.AJAX_FAIL_NOT_FOUND, message="页面不存在")
