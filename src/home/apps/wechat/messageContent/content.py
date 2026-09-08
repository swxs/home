from wechatpy.replies import TextReply

TEMPLATE = """\
您可以输入 `/` 获取本帮助提示:
1. 输入 `/早上好` 获取开始新的一天
2. 输入 `/随机图片` 获取随机图片
"""


class Content:
    name = "/"

    def __init__(self, db) -> None:
        self.db = db

    async def get_reply(self, message, token_schema):
        return TextReply(content=TEMPLATE, message=message)
