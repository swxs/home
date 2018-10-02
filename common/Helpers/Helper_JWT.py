# File    : Helper_JWT.py
# Author  : gorden
# Time    : 2018/8/31 10:21

from itsdangerous import TimedJSONWebSignatureSerializer as jwt
from itsdangerous import SignatureExpired, BadSignature
import time
import settings
from common.Helpers.DBHelper_Redis import RedisDBHelper

REFRESH_TOKEN_EXPIRE = 24 * 3600
ACCESS_TOKEN_EXPIRE = 3600


class AuthCenterError(object):
    E_NONE = 0x00  # indicates OK
    E_TOKEN_EXPIRED = 0x01
    E_TOKEN_BADSIGN = 0x02
    E_TOKEN_INVALID = 0x03

    errMap = dict()
    errMap[E_NONE] = u"成功"
    errMap[E_TOKEN_EXPIRED] = u"签名过期"
    errMap[E_TOKEN_BADSIGN] = u"签名不正确"
    errMap[E_TOKEN_INVALID] = u"Token无效"

    @classmethod
    def getErrorMsg(cls, errNo):
        return cls.errMap.get(errNo, "无效错误码")


class BlockTokenHelper(object):
    block_list = []
    client = RedisDBHelper(dbbase=settings.REDIS_TOKEN_BLOCK_DB).client

    @classmethod
    def append_block_token(cls, token):
        cls.client.set(f"token_{token}", True, ACCESS_TOKEN_EXPIRE)

    @classmethod
    def is_blocked(cls, token):
        return cls.client.get(f"token_{token}") != None


class AuthCenter(object):
    @classmethod
    def _encode(self, **kwargs):
        secret_key = kwargs.get("secret_key")
        salt = kwargs.get("salt")
        expireTime = kwargs.get("expire", None)
        data = kwargs.get("playload", {})
        gen = jwt(secret_key=secret_key, salt=salt, expires_in=expireTime)
        data.update({"iat": time.time()})
        return gen.dumps(data)

    @classmethod
    def _decode(self, token, secret_key, salt):
        gen = jwt(secret_key=secret_key, salt=salt)
        try:
            data = gen.loads(token)
        except SignatureExpired:
            return [AuthCenterError.E_TOKEN_EXPIRED, None]
        except BadSignature:
            return [AuthCenterError.E_TOKEN_BADSIGN, None]
        except Exception as e:
            return [AuthCenterError.E_TOKEN_INVALID, None]
        return [AuthCenterError.E_NONE, data]

    @classmethod
    def gen_access_token(cls, **kwargs):
        # use the default expire time(1 hour)
        expire = kwargs.pop("expire", ACCESS_TOKEN_EXPIRE)
        kwargs.update({"expire": expire})
        old_token = kwargs.pop("token", None)
        # push the old token into block list to disable it.
        if old_token:
            BlockTokenHelper.append_block_token(old_token)
        return cls._encode(**kwargs).decode()

    @classmethod
    def gen_refresh_token(cls, **kwargs):
        kwargs.update({"expire": REFRESH_TOKEN_EXPIRE})
        return cls._encode(**kwargs).decode()

    @classmethod
    def identify(cls, token, secret_key=settings.SECRET_KEY, salt=settings.SALT):
        if BlockTokenHelper.is_blocked(token):
            return [AuthCenterError.E_TOKEN_INVALID, None]
        return cls._decode(token, secret_key, salt)

    @classmethod
    def authenticate(cls, username, password, authHandler):
        if not callable(authHandler):
            return [False, None, None]
        handler_res = authHandler(username, password)
        if not handler_res:
            return [False, None, None]
        user = handler_res.pop("user_data")
        access_token = cls.gen_access_token(**handler_res)
        refresh_token = cls.gen_refresh_token(**handler_res)
        return [True, access_token, refresh_token, user]
