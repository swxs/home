import uuid

from bson import ObjectId
from wechatpy.replies import ImageReply, TextReply

from apps.system.dao.user import User

# 通用方法
from commons.Helpers import gumengya_async, imgurl_helper, wechat_helper

# 本模块方法
from .content import Content


class PictureContent(Content):
    name = "/随机图片"

    @classmethod
    async def get_reply(cls, message, token_schema):
        content = f'您好，该功能暂未开发完成！'

        if token_schema.user_id:
            user = await User.find_one(
                finds={"id": ObjectId(token_schema.user_id)},
            )
            if user:
                # 获取随即图片
                buffer = await gumengya_async.get_mving()
                # 获取路径
                filepath = await imgurl_helper.upload_image(buffer, filename=f"{str(uuid.uuid4())}.jpg")
                # 上传微信
                media_id = await wechat_helper.upload_image(filepath)
                # 返回
                return ImageReply(media_id=media_id, message=message)

        return TextReply(content=content, message=message)
