from api.BaseConsts import HTTP_STATUS
from common.Exceptions.ApiException import ApiException


class ApiRedirectException(ApiException):
    def __init__(self, url=None):
        super(ApiRedirectException, self).__init__(code=HTTP_STATUS.AJAX_SUCCESS)
        self.url = url
