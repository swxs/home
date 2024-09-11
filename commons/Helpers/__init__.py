import core

# 本模块方法
from . import (
    ApiHelper_gumengya,
    ApiHelper_imgurl,
    ApiHelper_million365,
    ApiHelper_reader,
    ApiHelper_vvhan,
    ApiHelper_wechat,
    Helper_JWT,
    Helper_encryption,
)

encryption = Helper_encryption.Encryption(
    salt="b8862e668e5abbc99d8390347e7ac749",
)

tokener = Helper_JWT.Helper_JWT(
    key=core.config.JWT_SECRET_KEY,
    timeout=core.config.JWT_TIMEOUT,
)

refresh_tokener = Helper_JWT.Helper_JWT(
    key=core.config.JWT_SECRET_KEY,
    timeout=core.config.JWT_REFRESH_TIMEOUT,
)

wechat_helper = ApiHelper_wechat.WechatHelper(
    appid=core.config.WECHAT_APPID,
    appsecret=core.config.WECHAT_APPSECRET,
)

imgurl_helper = ApiHelper_imgurl.ImgurlHelper(
    uid=core.config.IMAGEURL_UID,
    token=core.config.IMAGEURL_TOKEN,
)

reader_async_helper = ApiHelper_reader.ReaderAsyncHelper(
    username='swxs',
    password='D6051da2199b',
)

gumengya_async_helper = ApiHelper_gumengya.GumengyaAsyncHelper()

vvhan_async_helper = ApiHelper_vvhan.VVhanAsyncHelper()

million365_async_helper = ApiHelper_million365.Million365AsyncHelper()
