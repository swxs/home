from common.ApiExceptions.ApiException import ApiException


class ApiCommonException(ApiException):
    '''
        非常规错误, 自定义返回内容
    '''

    def __init__(self, message=None, data=None):
        super(ApiCommonException, self).__init__(message=message, data=data)
