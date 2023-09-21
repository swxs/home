import io

import aiohttp


class GumengyaAsync:
    def __init__(self, domain):
        self.domain = domain
        self.cookie = None

    async def get_mving(self):
        # 调用获取列表的URL和参数
        api_url = f'{self.domain}/Api/MvImg?format=image'

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    buffer = io.BytesIO(await response.read())
                    return buffer
                else:
                    return None
