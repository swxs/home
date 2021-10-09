import enum
from core import config
from . import DBHelper_Redis
from . import DBHelper_Memcache
from . import Helper_mongodb_dumper
from . import Helper_JWT


class RegEnum(enum.Enum):
    ALL = r'.*'

    USERNAME = r'[a-zA-Z0-9_\-]{1,}'
    PASSWORD = r'[a-zA-Z0-9]{6,16}'
    CHANGED_PASSWORD = r'[0-9a-f]{32}'
    EMAIL = r'([a-zA-Z0-9_\.\-])+\@([a-zA-Z0-9\-])+(\.([a-zA-Z0-9]{2,6}))+'
    MOBILE = r'(1[3-9][0-9])[0-9]{8}'
    PHONE = r'(\(((010)|(021)|(0\d{3,4}))\)( ?)([0-9]{7,8}))|((010|021|0\d{3,4}))([- ]?)([0-9]{7,8})|([0-9]{7,8})'
    PHONE_COMMON = r'([0-9]{3}[_ -][0-9]{8}|[0-9]{4}-[0-9]{7}|[0-9]{8}|1[0-9]{10})'

    COLUMN_ID = r'[a-fA-F0-9]{24}'

    FORM_GET = r'application/x-www-form-urlencoded'
    FORM_FILE = r'multipart/form-data'
    HTML_TAG = r'</?(span|tr|hr|br|p|script)/?>'
    REQUEST_HEADER = r'httputil'

    CH = r'[^\u0000-\u00FF]*'
    NUMBER = r'([-]?[0-9]+(\.[0-9]+){0,1})'
    MONTH = r'(0?[1-9]|1[0-2])'
    DAY = r'((0?[1-9])|((1|2)[0-9])|(3[01]))'
    TIME = r'(0?[1-9]|1[0-9]|2[0-4])((:|-|\/|\\)(0?[0-9]|[1-5][0-9])){2}'
    DATE = r'[1-9][0-9]{0,3}(?:年|\||\\|\/|\s|,|、|-)(0?[1-9]|1[0-2])(?:月|\||\\|\/|\s|,|、|-)((0?[1-9])|((1|2)[0-9])|(3[01]))日?'
    BIRTHDAY = r'(19|20)[0-9]{2}(:|-|\/|\\)(((0?[1-9]|1[0-2])(:|-|\/|\\)(0?[1-9]|1[0-9]|2[0-9]))|((0?[13-9]|1[0-2])(:|-|\/|\\)(30))|((0?[13578]|1[02])(:|-|\/|\\)(31)))'
    CREDIT = '[1-9][0-9]{5}[1-9][0-9]{3}((0[0-9])|(1[0-2]))(([0|1|2][0-9])|3[0-1])[0-9]{3}([0-9]|x|X)'
    URL = r'((http|ftp|https)://)?(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}(\.[0-9]{1,3}){3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?'
    IPV4AGENT = r'(192\.168\.|169\.254\.|10\.|172\.(1[6-9]|2[0-9]|3[01]))'
    IPV4 = r'[0-9]{1,3}(\.[0-9]{1,3}){3}'
    IPV6 = r'[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})'


redis_helper = DBHelper_Redis.RedisDBHelper(
    db=config.REDIS_DB, host=config.REDIS_HOST, port=config.REDIS_PORT, password=config.REDIS_PASSWORD
)

memcache_helper = DBHelper_Memcache.MemcacheDBHelper(host=config.MEMCACHE_HOST, port=config.MEMCACHE_PORT)

mongodb_dumper_helper = Helper_mongodb_dumper.MongodbDumperHelper(
    config.MONGODB_ADDRESS,
    config.MONGODB_PORT,
    config.MONGODB_DBNAME,
    config.MONGODB_USERNAME,
    config.MONGODB_PASSWORD,
    config.MONGODB_AUTHDB,
    config.STATIC_DBBACK_PATH,
)

tokener = Helper_JWT.AuthTokner(key=config.JWT_SECRET_KEY, timeout=config.JWT_TIMEOUT)
refresh_tokener = Helper_JWT.AuthTokner(key=config.JWT_SECRET_KEY, timeout=config.JWT_REFRESH_TIMEOUT)
