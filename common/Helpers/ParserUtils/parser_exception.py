class SyntaxException(Exception):
    def __init__(self, msg="一般错误"):
        self.msg = msg

    def __str__(self):
        return f"语法错误: {self.msg}"