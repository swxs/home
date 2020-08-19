class BaseInfo:
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
        return BaseInfo(message=new_message, data=new_data, status=new_status, code=new_code, template=new_template)

    def __str__(self):
        return self.template.format(message=self.message)


class Info:
    Base = BaseInfo()

    NotLogin = BaseInfo(code=101, template="用户未登录")
    TokenLost = BaseInfo(code=111, template="Token未设置")
    TokenIllegal = BaseInfo(code=112, template="Token非法")
    TokenTimeout = BaseInfo(code=113, template="Token已过期")
    Permission = BaseInfo(code=121, template="没有权限")
    PageNotFound = BaseInfo(code=131, template="页面不存在")

    ParamsValidate = BaseInfo(code=201, template="参数不合法: {message}")
    Existed = BaseInfo(code=211, template="资源已存在: {message}")
    NotExist = BaseInfo(code=212, template="资源不存在: {message}")
    DeleteInhibit = BaseInfo(code=221, template="对象不可删除: {message}")


class ApiBaseException(Exception):
    def __init__(self, info):
        self.code = info.code
        self.template = info.template
        self.message = info.message
        self.data = info.data
        self.status = info.status

    def __str__(self):
        return self.template.format(message=self.message)


class ApiException(ApiBaseException):
    def __init__(self, info=None, **kwargs):
        if info is None:
            info = Info.Base
        info = info.update(**kwargs)
        super().__init__(info)


class ApiUnknowException(ApiBaseException):
    def __init__(self, e, info=None, **kwargs):
        if info is None:
            info = Info.Base
        info = info.update(data=e, message=str(e))
        super().__init__(info)
