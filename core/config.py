# -*- coding: utf-8 -*-

from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", False)

XSRF = env.str("XSRF", '__xsrf')
DEFAULT_LOCAL = env.str("DEFAULT_LOCAL", 'zh_CN')  # 默认语言
ACCESS_TOKEN_EXPIRE = env.int("ACCESS_TOKEN_EXPIRE", 60 * 60 * 2)
REFRESH_TOKEN_EXPIRE = env.int("REFRESH_TOKEN_EXPIRE", 60 * 60 * 24 * 7)
SUPER_PASSWORD = env.str("SUPER_PASSWORD", 'bc8720e67deb87b2a32131b07605813f')
SECRET_KEY = env.str("SECRET_KEY", '2f3c330a-7557-4705-9a61-8a4cc8d8698c')
SALT = env.str("SALT", 'cf70538d-46a6-47f7-bc99-51c3e45126ea')

JWT_SECRET_KEY = env.str("JWT_SECRET_KEY", '7f8512a4-afe7-4941-a0c0-62e75dc8edd4')  # 密钥
JWT_TIMEOUT = env.int("JWT_TIMEOUT", 2 * 60 * 60)  # 超时时间，单位: s
JWT_REFRESH_TIMEOUT = env.int("JWT_REFRESH_TIMEOUT", 7 * 24 * 60 * 60)  # 超时时间，单位: s

SITE_PROTOCOL = env.str("SITE_PROTOCOL", 'http')
SITE_DOMAIN = env.str("SITE_DOMAIN", '127.0.0.1')
SITE_PORT = env.int("SITE_PORT", 8088)

MONGODB_ADDRESS = env.str("MONGODB_ADDRESS", '127.0.0.1')
MONGODB_PORT = env.int("MONGODB_PORT", 27017)
MONGODB_URI = f'{MONGODB_ADDRESS}:{MONGODB_PORT}'
MONGODB_DBNAME = env.str("MONGODB_DBNAME", 'home')
MONGODB_USERNAME = env.str("MONGODB_USERNAME", None)
MONGODB_PASSWORD = env.str("MONGODB_PASSWORD", None)
MONGODB_AUTHDB = env.str("MONGODB_AUTHDB", None)

REDIS_HOST = env.str("REDIS_HOST", '127.0.0.1')
REDIS_PORT = env.int("REDIS_PORT", 6379)
REDIS_DB = env.int("REDIS_DB", 0)
REDIS_PASSWORD = env.str("REDIS_PASSWORD", None)

MEMCACHE_HOST = env.str("MEMCACHE_HOST", '127.0.0.1')
MEMCACHE_PORT = env.int("MEMCACHE_PORT", 11211)
MEMCACHE_EXPIRE_TIME = env.int("MEMCACHE_EXPIRE_TIME", 120)

RPC_SERVER_HOST = env.str("RPC_SERVER_HOST", '127.0.0.1')
RPC_SERVER_PORT = env.int("RPC_SERVER_PORT", 6000)

WECHAT_TOKEN = env.str("WECHAT_TOKEN", "")
WECHAT_ENCODING_AES_KEY = env.str("WECHAT_ENCODING_AES_KEY", "")
WECHAT_APPID = env.str("WECHAT_APPID", "")
WECHAT_APPSECRET = env.str("WECHAT_APPSECRET", "")

MAIL_SERVER_IP = env.str("MAIL_SERVER_IP", "")
MAIL_SERVER_USER = env.str("MAIL_SERVER_USER", "")
MAIL_SERVER_USER_MAIL = env.str("MAIL_SERVER_USER_MAIL", "")
MAIL_SENDER_NAME = env.str("MAIL_SENDER_NAME", "")
