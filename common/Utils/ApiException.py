class ApiException(Exception):
    def __init__(self, info):
        self.code = info.code
        self.template = info.template
        self.message = info.message
        self.data = info.data
        self.status = info.status

    def __str__(self):
        return self.template.format(message=self.message)

class ApiCommonException(ApiException):
    def __init__(self, info, **kwargs):
        info = info.update(**kwargs)
        super().__init__(info)

class ApiUnknowException(ApiException):
    def __init__(self, e, **kwargs):
        info = BaseExceptionInfo(message=str(e))
        super().__init__(info)

class BaseExceptionInfo:
    """
    异常信息
    """
    def __init__(self, code=-1, template="{message}", message="", data=None, status=200):
        self.code = code
        self.template = template
        self.message = message
        self.data = data
        self.status = status
    
    def update(self, code=None, template=None, message=None, data=None, status=None):
        new_code = code if code is not None else self.code
        new_template = template if template is not None else self.template
        new_message = message if message is not None else self.message
        new_data = data if data is not None else self.data
        new_status = status if status is not None else self.status
        return BaseExceptionInfo(new_code, new_template, new_message, new_data, new_status)
        
    def __str__(self):
        return self.template.format(message=self.message)

class CommmonExceptionInfo:
    BaseException = BaseExceptionInfo()

    NotLoginException = BaseExceptionInfo(101, "用户未登录", "{message}")
    PermissionException = BaseExceptionInfo(102, "没有权限", "{message}")
    TokenIllegalException = BaseExceptionInfo(103, "Token非法", "{message}")
    TokenTimeoutException = BaseExceptionInfo(104, "Token已过期", "{message}")

    ValidateException = BaseExceptionInfo(201, "", "参数不合法: {message}")
    DeleteInhibitException = BaseExceptionInfo(202, "", "对象不可删除: {message}")
    PageNotFoundException = BaseExceptionInfo(204, "页面不存在", "{message}")

    ExistedException = BaseExceptionInfo(301, "", "资源已存在: {message}")
    NotExistException = BaseExceptionInfo(302, "", "资源不存在: {message}")
