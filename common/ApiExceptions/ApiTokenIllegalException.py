from api.BaseConsts import HTTP_STATUS
from common.ApiExceptions import ApiException


class ApiTokenIllegalException(ApiException):
    def __init__(self):
        super(ApiTokenIllegalException, self).__init__(code=HTTP_STATUS.AJAX_TOKEN_Illegal, message="Token非法")