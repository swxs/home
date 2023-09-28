import aiohttp


class ReaderAsyncHelper:
    def __init__(self, username, password, domain):
        self.username = username
        self.password = password
        self.domain = domain
        self.cookie = None

    async def login_and_get_reader(self):
        # 创建aiohttp客户端会话
        async with aiohttp.ClientSession() as session:
            if self.cookie is None:
                # 登录接口参数
                login_url = f'{self.domain}/api/auth/signin'
                login_payload = {
                    'username': self.username,
                    'password': self.password,
                }

                # 调用登录接口进行登录
                async with session.post(login_url, json=login_payload) as login_response:
                    # 获取返回的cookie
                    self.cookies = login_response.cookies

            # 调用获取列表的URL和参数
            api_url = f'{self.domain}/api/page/list'
            api_params = {
                'asc': 'false',
                'connectorType': '1',
                'count': '20',
                'markRead': 'false',
                'sort': 'CONNECTED_AT',
            }

            # 使用获取的cookie携带请求调用接口2
            async with session.get(api_url, params=api_params, cookies=self.cookies) as response:
                # 处理接口2的响应数据
                data = await response.json()
                return data
