# -*- coding: utf-8 -*-

import os
from common.Utils.dir_path import get_dir_path

OS = 'linux'
DEBUG = False
DB_TRIGGER_FLAG = False
SECRET_KEY = 'd96f097c-4b1b-4867-3859-375830cd69c4'

SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_PROTOCOL = 'http'
SITE_DOMAIN = '127.0.0.1'
SITE_PORT = 8088
SITE_URL = '{0}://{1}:{2}'.format(SITE_PROTOCOL, SITE_DOMAIN, SITE_PORT)

STATIC_PATH = get_dir_path(SITE_ROOT, 'static')
TEMPLATE_PATH = get_dir_path(SITE_ROOT, 'template')
DATAFILE_PATH = get_dir_path(SITE_ROOT, 'data_file')
TRANSLATIONS_PATH = get_dir_path(SITE_ROOT, "translations")
STATIC_ZIPFILE_PATH = os.path.join(SITE_ROOT, 'static', 'zipfile')

MONGODB_ADDRESS = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'home'

MEMCACHE_SERVER = '127.0.0.1'
MEMCACHE_PORT = 11211
MEMCACHE_EXPIRE_TIME = 120
MEMCACHE_HOSTS = ('{0}:{1}'.format(MEMCACHE_SERVER, MEMCACHE_PORT),)

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None
REDIS_LOG_MAIL_LIST_NAME = []

XSRF = '__xsrf'

SUPER_PASSWORD = 'bc8720e67deb87b2a32131b07605813f'

WECHAT_ACCESS_TOKEN_URL = ""
WECHAT_REFRESH_ACCESS_TOKEN_URL = ""
WECHAT_USERINFO_URL = ""
WECHAT_APPID = ""
WECHAT_SECRET = ""

MAIL_SERVER_IP = ""
MAIL_SERVER_USER = ""
MAIL_SERVER_USER_MAIL = ""
MAIL_SENDER_NAME = ""

try:
    from local_settings import *
except:
    print('load local settings faild.')

if SITE_PORT == 80:
    SITE_URL = '%s://%s' % (SITE_PROTOCOL, SITE_DOMAIN)
else:
    SITE_URL = '%s://%s:%s' % (SITE_PROTOCOL, SITE_DOMAIN, SITE_PORT)

# connect to mongodb
DB_CONNECTED = False


def connect_db(db_name=MONGODB_DBNAME):
    global DB_CONNECTED
    from mongoengine.connection import connect
    connect(db_name, host=MONGODB_ADDRESS, port=MONGODB_PORT, is_slave=False, slaves=None)
    DB_CONNECTED = True


connect_db()
if DB_TRIGGER_FLAG:
    from db.model_modify_trigger import bind_signals
    bind_signals()

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
