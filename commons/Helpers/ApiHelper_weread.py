import io
from http.cookies import SimpleCookie

import aiohttp
from requests.utils import cookiejar_from_dict

from web.exceptions.http_500_internal_server_error_exception import (
    Http500InternalServerErrorException,
)

DOMAIN = "https://weread.qq.com"
DOMAIN = "https://i.weread.qq.com"
WEREAD_NOTEBOOKS_URL = f"{DOMAIN}/user/notebooks"
WEREAD_BOOKMARKLIST_URL = f"{DOMAIN}/book/bookmarklist"
WEREAD_CHAPTER_INFO = f"{DOMAIN}/book/chapterInfos"
WEREAD_READ_INFO_URL = f"{DOMAIN}/book/readinfo"
WEREAD_REVIEW_LIST_URL = f"{DOMAIN}/review/list"
WEREAD_BOOK_INFO = f"{DOMAIN}/book/info"


class WereadHelper:
    def __init__(self, cookie):
        self.cookie = cookie
        self.cookiejar = self.parse_cookie_string(self.cookie)

    def parse_cookie_string(self, cookie_string):
        cookie = SimpleCookie()
        cookie.load(cookie_string)
        cookies_dict = {}
        cookiejar = None
        for key, morsel in cookie.items():
            cookies_dict[key] = morsel.value
        cookiejar = cookiejar_from_dict(cookies_dict, cookiejar=aiohttp.CookieJar(), overwrite=True)
        return cookiejar

    async def get_book_info_list(self):
        # 调用获取列表的URL和参数
        async with aiohttp.ClientSession(DOMAIN, cookie_jar=self.cookiejar) as session:
            async with session.get(WEREAD_NOTEBOOKS_URL) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "WereadHelper Error",
                    )
                print(await response.read())

            async with session.get(WEREAD_BOOKMARKLIST_URL, cookies=self.cookiejar) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "WereadHelper Error",
                    )
                print(await response.read())

            async with session.get(WEREAD_CHAPTER_INFO, cookie_jar=self.cookiejar) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "WereadHelper Error",
                    )
                print(await response.read())

            async with session.get(WEREAD_READ_INFO_URL, cookie_jar=self.cookiejar) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "WereadHelper Error",
                    )
                print(await response.read())

            async with session.get(WEREAD_REVIEW_LIST_URL, cookie_jar=self.cookiejar) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "WereadHelper Error",
                    )
                print(await response.read())

            async with session.get(WEREAD_BOOK_INFO, cookie_jar=self.cookiejar) as response:
                if response.status != 200:
                    raise Http500InternalServerErrorException(
                        Http500InternalServerErrorException.HelperServerError,
                        "WereadHelper Error",
                    )
                print(await response.read())
