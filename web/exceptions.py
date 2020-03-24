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
    def __init__(self, message="", data=None, status=200, code=-1, template="{message}"):
        self.code = code
        self.template = template
        self.message = message
        self.data = data
        self.status = status
    
    def update(self, message=None, data=None, status=None, code=None, template=None):
        new_code = code if code is not None else self.code
        new_template = template if template is not None else self.template
        new_message = message if message is not None else self.message
        new_data = data if data is not None else self.data
        new_status = status if status is not None else self.status
        return BaseExceptionInfo(message=new_message, data=new_data, status=new_status, code=new_code, template=new_template)
        
    def __str__(self):
        return self.template.format(message=self.message)

class CommmonExceptionInfo:
    BaseException = BaseExceptionInfo()

    NotLoginException = BaseExceptionInfo(code=101, template="用户未登录")
    PermissionException = BaseExceptionInfo(code=102, template="没有权限")
    TokenIllegalException = BaseExceptionInfo(code=103, template="Token非法")
    TokenTimeoutException = BaseExceptionInfo(code=104, template="Token已过期")

    ValidateException = BaseExceptionInfo(code=201, template="参数不合法: {message}")
    DeleteInhibitException = BaseExceptionInfo(code=202, template="对象不可删除: {message}")
    PageNotFoundException = BaseExceptionInfo(code=204, template="页面不存在")
    
    ExistedException = BaseExceptionInfo(code=301, template="资源已存在: {message}")
    NotExistException = BaseExceptionInfo(code=302, template="资源不存在: {message}")
