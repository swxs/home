from bson import ObjectId

from apps.system.dao.user import User

# 通用方法
from commons.Helpers import reader_async

# 本模块方法
from .content import Content


class MorningContent:
    name = "/早上好"

    @classmethod
    async def get_result(cls, token_schema):
        content = f'您好，该功能暂未开发完成！'

        if token_schema.user_id:
            user = await User.find_one(
                finds={"id": ObjectId(token_schema.user_id)},
            )
            huntly_list = await reader_async.login_and_get_reader()
            if huntly_list:
                content = f'{user.username}您好，目前有{len(huntly_list)}文章等待阅读'

        return content
