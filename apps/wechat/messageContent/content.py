from wechatpy.replies import TextReply

TEMPLATE = """\
您可以输入 `/` 获取本帮助提示:
1. 输入 `/早上好` 获取开始新的一天
2. 输入 `/随机图片` 获取随机图片
"""


class Content:
    name = "/"

    @classmethod
    async def get_reply(cls, message, token_schema):
        return TextReply(content=TEMPLATE, message=message)
