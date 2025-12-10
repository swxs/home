from bson import ObjectId
from wechatpy.replies import TextReply

# 通用方法
from commons.Helpers import reader_async_helper

from apps.system.repositories.user_repository import UserRepository

# 本模块方法
from .content import Content

TEMPLATE = """\
您好，该功能暂未开发完成！
"""


class MorningContent(Content):
    name = "/早上好"

    async def get_reply(self, message, token_schema):
        content = TEMPLATE

        if token_schema.user_id:
            user_repo = UserRepository(self.db)
            user = await user_repo.find_one(
                token_schema.user_id,
            )
            if user:
                # 获取待读文章数量, 并返回
                huntly_list = await reader_async_helper.login_and_get_reader()
                if huntly_list:
                    content = f"{user.username}您好，目前有{len(huntly_list)}文章等待阅读"
                    return TextReply(content=content, message=message)

        return TextReply(content=content, message=message)
