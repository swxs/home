import core

# 本模块方法
from . import (
    ApiHelper_gumengya,
    ApiHelper_imgurl,
    ApiHelper_million365,
    ApiHelper_oss2,
    ApiHelper_reader,
    ApiHelper_vvhan,
    ApiHelper_wechat,
    Helper_JWT,
    Helper_encryption,
)

encryption = Helper_encryption.Encryption(
    salt=core.config.PASSWORD_SALT,
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
    username=core.config.WECHAT_READER_USERNAME,
    password=core.config.WECHAT_READER_PASSWORD,
)

gumengya_async_helper = ApiHelper_gumengya.GumengyaAsyncHelper()

vvhan_async_helper = ApiHelper_vvhan.VVhanAsyncHelper()

million365_async_helper = ApiHelper_million365.Million365AsyncHelper()

oss2_helper = ApiHelper_oss2.Oss2Helper(
    key_id=core.config.OSS_ACCESS_KEY_ID,
    secret=core.config.OSS_ACCESS_KEY_SECRET,
    host=core.config.OSS_HOST,
    bucket=core.config.OSS_BUCKET,
    root_dir=core.config.OSS_ROOT_DIR,
)
