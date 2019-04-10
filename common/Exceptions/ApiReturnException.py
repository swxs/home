from api.BaseConsts import HTTP_STATUS
from common.Exceptions.ApiException import ApiException


class ApiReturnException(ApiException):
    def __init__(self, data=None):
        '''
        无错误， 在不能返回时使用， eg：tornado（py2）
        :param errmsg:
        :param data:
        '''
        super(ApiReturnException, self).__init__(code=HTTP_STATUS.AJAX_SUCCESS, data=data)
