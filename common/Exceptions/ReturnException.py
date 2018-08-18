from api.consts import const
from common.Exceptions.ApiException import ApiException

class ReturnException(ApiException):
    def __init__(self, errmsg=None, data=None):
        self.code = const.AJAX_SUCCESS
        self.message = ""
        self.data = data

    def __str__(self):
        return self.message