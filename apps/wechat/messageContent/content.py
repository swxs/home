class Content:
    name = "/"

    @classmethod
    async def get_result(cls, user):
        return f"""\n
        您可以输入 `/` 获取本帮助提示:
        1. 输入 `/早上好` 获取开始新的一天
        2. 输入 `/图片` 获取随机图片
        """
