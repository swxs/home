# File    : Helper_JWT.py
# Author  : gorden
# Time    : 2018/8/31 10:21

import time
from itsdangerous import TimedJSONWebSignatureSerializer as jwt
from itsdangerous import SignatureExpired, BadSignature

import settings
from common.Helpers.DBHelper_Redis import redis_helper
from common.Utils import log_utils
from web.exceptions import ApiCommonException, CommmonExceptionInfo

log = log_utils.getLogger("Helper_JWT")


class BlockTokenHelper(object):
    block_list = []

    @classmethod
    def append_block_token(cls, token):
        redis_helper.set(f"token_{token}", True, settings.ACCESS_TOKEN_EXPIRE)

    @classmethod
    def is_blocked(cls, token):
        return redis_helper.get(f"token_{token}") != None


class AuthCenter(object):
    @classmethod
    def _encode(self, **kwargs):
        secret_key = kwargs.get("secret_key")
        salt = kwargs.get("salt")
        expire = kwargs.get("expire", None)
        gen = jwt(secret_key=secret_key, salt=salt, expires_in=expire)

        data = kwargs.get("playload", {})
        data.update({"iat": time.time()})
        return gen.dumps(data)

    @classmethod
    def _decode(self, token, secret_key, salt):
        gen = jwt(secret_key=secret_key, salt=salt)
        try:
            return gen.loads(token)
        except SignatureExpired:
            raise ApiTokenIllegalException(CommmonExceptionInfo.TokenTimeoutException)
        except BadSignature:
            raise ApiTokenIllegalException(CommmonExceptionInfo.TokenIllegalException)
        except Exception as e:
            log.error(f"unknow error: {e}")
            raise ApiTokenIllegalException(CommmonExceptionInfo.TokenIllegalException)

    @classmethod
    def gen_access_token(cls, **kwargs):
        kwargs.update(dict(expire=settings.ACCESS_TOKEN_EXPIRE))
        # token = kwargs.pop("token", None)
        # if token:
        #     BlockTokenHelper.append_block_token(token)
        return cls._encode(**kwargs).decode()

    @classmethod
    def gen_refresh_token(cls, **kwargs):
        kwargs.update({"expire": settings.REFRESH_TOKEN_EXPIRE})
        return cls._encode(**kwargs).decode()

    @classmethod
    def identify(cls, token, secret_key=settings.SECRET_KEY, salt=settings.SALT):
        if BlockTokenHelper.is_blocked(token):
            raise ApiTokenIllegalException(CommmonExceptionInfo.TokenTimeoutException)
        return cls._decode(token, secret_key, salt)

    @classmethod
    def authenticate(cls, user):
        data = {
            "salt": settings.SALT,
            "secret_key": settings.SECRET_KEY,
            "playload": {"id": user.id},
        }
        access_token = cls.gen_access_token(**data)
        refresh_token = cls.gen_refresh_token(**data)
        return access_token, refresh_token
