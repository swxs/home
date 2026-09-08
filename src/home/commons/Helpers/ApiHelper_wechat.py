from wechatpy import WeChatClient


class WechatHelper:
    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret
        self.client = WeChatClient(self.appid, self.appsecret)

    async def upload_image(self, buffer):
        result = self.client.media.upload('image', buffer)
        media_id = result['media_id']
        return media_id
