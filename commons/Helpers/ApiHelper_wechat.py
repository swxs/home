from wechatpy import WeChatClient


class WechatHelper:
    def __init__(self, appid, appsecret):
        self.appid = appid
        self.appsecret = appsecret
        self.client = WeChatClient(self.appid, self.appsecret)

    async def upload_image(self, file_path):
        try:
            result = self.client.media.upload('image', file_path)
            media_id = result['media_id']
            return media_id
        except Exception as e:
            pass
