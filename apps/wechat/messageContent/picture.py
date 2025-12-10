import uuid

from bson import ObjectId
from wechatpy.replies import ImageReply, TextReply

# 通用方法
from commons.Helpers import gumengya_async_helper, wechat_helper

from apps.system.repositories.user_repository import UserRepository

# 本模块方法
from .content import Content


class PictureContent(Content):
    name = "/随机图片"

    async def get_reply(self, message, token_schema):
        content = f"您好，该功能暂未开发完成！"

        if token_schema.user_id:
            user_repo = UserRepository(self.db)
            user = await user_repo.find_one(
                token_schema.user_id,
            )
            if user:
                # 获取随即图片
                buffer = await gumengya_async_helper.get_mving()
                # 上传微信
                media_id = await wechat_helper.upload_image((f"{str(uuid.uuid4())}.jpg", buffer, "image/jpeg"))
                # 返回
                return ImageReply(media_id=media_id, message=message)

        return TextReply(content=content, message=message)
