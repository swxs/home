# File    : Helper_JWT.py
# Author  : gorden
# Time    : 2018/8/31 10:21

"""
简介
----------
依赖 pyjwt 库
提供生成、解析JWT的方法


"""

import datetime

import jwt

DecodeError = jwt.DecodeError
InvalidSignatureError = jwt.InvalidSignatureError
ExpiredSignatureError = jwt.ExpiredSignatureError
ImmatureSignatureError = jwt.ImmatureSignatureError


class Helper_JWT(object):
    def __init__(
        self,
        key=None,
        timeout=60 * 60 * 2,
        issue='AuthTokener',
        algorithm="HS256",
        verify=True,
        leeway_time=60,
        json_encoder=None,
    ) -> None:
        if key is None:
            raise ValueError("you mast set a key!")
        self.key = key
        self.timeout = timeout
        self.issue = issue
        self.algorithm = algorithm
        self.verify = verify
        self.leeway_time = leeway_time
        self.json_encoder = json_encoder

    def encode(self, **kwargs):
        """
        简介
        ----------
        生成JWT

        :param kwargs:
            信息体

        返回
        ----------
            jwt[字节型]
        """
        utc_now = datetime.datetime.utcnow()
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
            json_encoder=self.json_encoder,
        )

    def decode(self, token):
        """
        简介
        ----------
        解析JWT

        参数
        ----------
        token :
            jwt[字节型]

        返回
        ----------

        """
        header = jwt.get_unverified_header(token if isinstance(token, bytes) else token.encode('utf-8'))
        payload = jwt.decode(
            token, key=self.key, verify=self.verify, leeway=self.leeway_time, algorithms=[self.algorithm]
        )
        del payload['exp']
        del payload['nbf']
        del payload['iat']
        del payload['iss']
        return header, payload
