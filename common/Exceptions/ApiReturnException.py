from api.consts import const
from common.Exceptions.ApiException import ApiException

class ApiReturnException(ApiException):
    def __init__(self, data=None):
        '''
        无错误， 在不能返回时使用， eg：tornado（py2）
        :param errmsg:
        :param data:
        '''
        self.code = const.AJAX_SUCCESS
        self.message = ""
        self.data = data

    def __str__(self):
        return self.message