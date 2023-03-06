class BaseHttpException(Exception):
    __slots__ = ("status_code", "code", "message", "data")

    def __init__(self, status_code, code, message, data=None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.data = data
