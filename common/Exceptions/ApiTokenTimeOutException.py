from api.consts.const import HTTP_STATUS
from common.Exceptions import ApiException


class ApiTokenTimeOutException(ApiException):
    def __init__(self):
        super(ApiTokenTimeOutException, self).__init__(code=HTTP_STATUS.AJAX_TOKEN_TIMEOUT, message="Token已过期")
