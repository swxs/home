# -*- coding: utf-8 -*-

import os
import logging
import logging.config
from commons.Utils.path_utils import get_dir_path

OS = 'linux'
DEBUG = False
XSRF = '__xsrf'
DEFAULT_LOCAL = 'zh_CN'
ACCESS_TOKEN_EXPIRE = 60 * 60 * 2
REFRESH_TOKEN_EXPIRE = 60 * 60 * 24 * 7
SUPER_PASSWORD = 'bc8720e67deb87b2a32131b07605813f'
SECRET_KEY = '2f3c330a-7557-4705-9a61-8a4cc8d8698c'
SALT = 'cf70538d-46a6-47f7-bc99-51c3e45126ea'

JWT_SECRET_KEY = '7f8512a4-afe7-4941-a0c0-62e75dc8edd4'  # 密钥
JWT_TIMEOUT = 2 * 60 * 60  # 超时时间，单位: s
JWT_REFRESH_TIMEOUT = 7 * 24 * 60 * 60  # 超时时间，单位: s

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_PROTOCOL = 'http'
SITE_DOMAIN = '127.0.0.1'
SITE_PORT = 8088

RPC_MODULE_LIST = []

LOG_PATH = get_dir_path(SITE_ROOT, 'logs')
STATIC_PATH = get_dir_path(SITE_ROOT, 'static')
DATAFILE_PATH = get_dir_path(SITE_ROOT, 'static', 'data_file')
STATIC_ZIPFILE_PATH = get_dir_path(SITE_ROOT, 'static', 'zipfile')
STATIC_DBBACK_PATH = get_dir_path(SITE_ROOT, 'static', 'dbback')
TEMP_PATH = get_dir_path(SITE_ROOT, 'temp')
TEMPLATE_PATH = get_dir_path(SITE_ROOT, 'template')
TRANSLATIONS_PATH = get_dir_path(SITE_ROOT, "translations")
SPIDER_LOG_PATH = get_dir_path(SITE_ROOT, 'model_spider', 'model_spider', 'logs')

INIT_SETTINGS_FILE = os.path.join(SITE_ROOT, "init.yaml")

MEMCACHE_HOST = '127.0.0.1'
MEMCACHE_PORT = 11211
MEMCACHE_EXPIRE_TIME = 120

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None
REDIS_TOKEN_BLOCK_DB = 3

MONGODB_ADDRESS = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'home'
MONGODB_USERNAME = None
MONGODB_PASSWORD = None
MONGODB_AUTHDB = None

MAIL_SERVER_IP = ""
MAIL_SERVER_USER = ""
MAIL_SERVER_USER_MAIL = ""
MAIL_SENDER_NAME = ""

WECHAT_ACCESS_TOKEN_URL = ""
WECHAT_REFRESH_ACCESS_TOKEN_URL = ""
WECHAT_USERINFO_URL = ""
WECHAT_APPID = ""
WECHAT_SECRET = ""

RPC_SERVER_HOST = '127.0.0.1'
RPC_SERVER_PORT = 6000

try:
    from local_settings import *  # noqa: F403
except Exception:
    print('load local settings faild.')

if SITE_PORT == 80:
    SITE_URL = f'{SITE_PROTOCOL}://{SITE_DOMAIN}'
else:
    SITE_URL = f'{SITE_PROTOCOL}://{SITE_DOMAIN}:{SITE_PORT}'

MEMCACHE_HOSTS = (f'{MEMCACHE_HOST}:{MEMCACHE_PORT}',)

DB_CONNECTED = False

script_path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(os.path.join(script_path, 'logging.ini'))


def connect_db_mysql():
    import asyncio
    import pymysql

    pymysql.install_as_MySQLdb()

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String, Text, MetaData, Table
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.orm import sessionmaker

    from sqlalchemy_aio import ASYNCIO_STRATEGY, TRIO_STRATEGY
    from sqlalchemy_aio.asyncio import AsyncioEngine

    engine = create_engine(
        "mysql://root:swxs@localhost/runoob", strategy=ASYNCIO_STRATEGY, encoding='latin1', echo=False
    )
    return engine


def connect_db(db_name=MONGODB_DBNAME, mock=False):
    global DB_CONNECTED
    from motor.motor_asyncio import AsyncIOMotorClient
    from umongo import Instance, Document, fields, ValidationError, set_gettext
    from umongo.marshmallow_bonus import SchemaFromUmongo

    db = AsyncIOMotorClient()[db_name]
    return Instance(db)


try:
    engine = connect_db_mysql()
except Exception:
    print("mysql db connect failed!")

try:
    MONGO_INSTANCE = connect_db()
except Exception:
    print("mongo db connect failed!")

settings = dict(
    cookie_secret=SECRET_KEY,
    login_url="/login/",
    template_path=TEMPLATE_PATH,
    static_path=STATIC_PATH,
    root_path=SITE_ROOT,
    xsrf_cookies=False,
    autoescape="xhtml_escape",
    debug=DEBUG,
    xheaders=True,
    translations=TRANSLATIONS_PATH,
    # static_url_prefix='', #启用CDN后可修改此定义, 例如: "http://cdn.abc.com/static/"
    pycket={
        'engine': 'memcached',
        'storage': {'servers': MEMCACHE_HOSTS},
        'cookies': {
            'expires_days': 6,
        },
    },
)

settings['pycket'] = {
    'engine': 'redis',
    'storage': {'host': REDIS_HOST, 'port': REDIS_PORT, 'db_sessions': 10, 'db_notifications': 11},
}
