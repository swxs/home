# File    : Helper_JWT.py
# Author  : gorden
# Time    : 2018/8/31 10:21

import jwt
import base64
import time
import datetime
from binascii import unhexlify
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as SignPKCS1_v1_5

JWT_SECRET_KEY = '6ec98328-133c-4c2f-933f-f5eadb49b9f3'  # 密钥
JWT_TIMEOUT = 2 * 60 * 60  # 超时时间，单位: s
JWT_ALGORITHM = "HS256"
JWT_VERIFY = True
JWT_TIMEOUT_LEEWAY_TIME = 60  # Token超时时间检验误差阀值，单位: s
JWT_ENCODER = None
JWT_ISSUER = 'AuthTokener'  # 发行者信息

InvalidSignatureError = jwt.InvalidSignatureError
ExpiredSignatureError = jwt.ExpiredSignatureError
ImmatureSignatureError = jwt.ImmatureSignatureError


class AuthTokner(object):
    def __init__(
        self,
        key=JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
        verify=JWT_VERIFY,
        timeout=JWT_TIMEOUT,
        leeway_time=JWT_TIMEOUT_LEEWAY_TIME,
        json_encoder=JWT_ENCODER,
        issue=JWT_ISSUER,
    ) -> None:
        self.key = key
        self.algorithm = algorithm
        self.verify = verify
        self.timeout = timeout
        self.leeway_time = leeway_time
        self.json_encoder = json_encoder
        self.issue = issue

    def encode(self, **kwargs):
        """
        生成json web token

        :param headers: token头信息
        :param json_encoder: json转化器
        :param kwargs:
        :return: jwt，字节型
        """
        utc_now = utc_now = datetime.datetime.utcnow()
        headers = {}
        payload = {
            'exp': utc_now + datetime.timedelta(seconds=self.timeout),
            'iat': utc_now,
            'nbf': utc_now,
            'iss': self.issue,
        }
        payload.update(kwargs)

        return jwt.encode(
            payload,
            key=self.key,
            algorithm=self.algorithm,
            headers=headers,
        ).decode('utf-8')

    def decode(self, token):
        header = jwt.get_unverified_header(token if isinstance(token, bytes) else token.encode('utf-8'))
        payload = jwt.decode(token, key=self.key, verify=self.verify, leeway=self.leeway_time)
        del payload['exp']
        del payload['nbf']
        del payload['iat']
        del payload['iss']
        return header, payload
