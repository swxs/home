# -*- coding: utf-8 -*-

import os
from common.Utils.dir_path import get_dir_path

OS = 'linux'
DEBUG = False
XSRF = '__xsrf'
DEFAULT_LOCAL = 'zh_CN'
SUPER_PASSWORD = 'bc8720e67deb87b2a32131b07605813f'
SECRET_KEY = 'd96f097c-4b1b-4867-3859-375830cd69c4'

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_PROTOCOL = 'http'
SITE_DOMAIN = '127.0.0.1'
SITE_PORT = 8088

MEMCACHE_HOST = '127.0.0.1'
MEMCACHE_PORT = 11211
MEMCACHE_EXPIRE_TIME = 120

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None

MONGODB_ADDRESS = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'home'

MAIL_SERVER_IP = ""
MAIL_SERVER_USER = ""
MAIL_SERVER_USER_MAIL = ""
MAIL_SENDER_NAME = ""

WECHAT_ACCESS_TOKEN_URL = ""
WECHAT_REFRESH_ACCESS_TOKEN_URL = ""
WECHAT_USERINFO_URL = ""
WECHAT_APPID = ""
WECHAT_SECRET = ""

LOG_PATH = get_dir_path(SITE_ROOT, 'logs')
STATIC_PATH = get_dir_path(SITE_ROOT, 'static')
TEMPLATE_PATH = get_dir_path(SITE_ROOT, 'template')
DATAFILE_PATH = get_dir_path(SITE_ROOT, 'data_file')
TRANSLATIONS_PATH = get_dir_path(SITE_ROOT, "translations")
STATIC_ZIPFILE_PATH = os.path.join(SITE_ROOT, 'static', 'zipfile')
SPIDER_LOG_PATH = os.path.join(SITE_ROOT, 'model_spider', 'model_spider', 'logs')

try:
    from local_settings import *
except:
    print('load local settings faild.')

if SITE_PORT == 80:
    SITE_URL = f'{SITE_PROTOCOL}://{SITE_DOMAIN}'
else:
    SITE_URL = f'{SITE_PROTOCOL}://{SITE_DOMAIN}:{SITE_PORT}'
MEMCACHE_HOSTS = (f'{MEMCACHE_HOST}:{MEMCACHE_PORT}',)

DB_CONNECTED = False


def connect_db(db_name=MONGODB_DBNAME):
    global DB_CONNECTED
    from mongoengine.connection import connect
    connect(db_name, host=MONGODB_ADDRESS, port=MONGODB_PORT, is_slave=False, slaves=None)
    DB_CONNECTED = True


connect_db()

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
        'storage': {
            'servers': MEMCACHE_HOSTS
        },
        'cookies': {
            'expires_days': 6,
        }
    }
)

settings['pycket'] = {
    'engine': 'redis',
    'storage': {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db_sessions': 10,
        'db_notifications': 11
    }
}
