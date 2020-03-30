# !/usr/bin/python
# @author: 'samuel.zhang'
# @datetime: 2019-02-27 11:36

import jwt
import base64
import datetime
from binascii import unhexlify
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as SignPKCS1_v1_5

CLAIM_TYPE = 'typ'  # 声明-类型
CLAIM_ALG = 'alg'  # 声明-加密/解密方式
CLAIM_EXP_TIME = 'exp'  # 声明-过期时间
CLAIM_NOT_BEFORE_TIME = 'nbf'  # 声明-校验时间不能在此设定时间之后
CLAIM_ISSUER = 'iss'  # 声明-发行者
CLAIM_ISSUED_AT = 'iat'  # 声明-发行时间
CLAIM_AUDIENCE = 'aud'  # 声明- 观众

JWT_SECRET_KEY = '6ec98328-133c-4c2f-933f-f5eadb49b9f3'  # 密钥
JWT_TIMEOUT = 2 * 60 * 60  # 超时时间，单位: s
JWT_TIMEOUT_LEEWAY_TIME = 60  # Token超时时间检验误差阀值，单位: s
JWT_ISSUER = 'SWXS'  # 发行者信息


def encode(key=JWT_SECRET_KEY, algorithm="HS256", headers=None, json_encoder=None, **kwargs) -> bytes:
    """
    生成json web token

    :param key: 签名密钥
    :param algorithm: 加密算法
    :param headers: token头信息
    :param json_encoder: json转化器
    :param kwargs:
    :return: jwt，字节型
    """
    utc_now = datetime.datetime.utcnow()
    payload = {
        CLAIM_EXP_TIME: utc_now + datetime.timedelta(seconds=kwargs.get("timeout", JWT_TIMEOUT)),
        CLAIM_ISSUED_AT: utc_now,
        CLAIM_NOT_BEFORE_TIME: utc_now,
        CLAIM_ISSUER: JWT_ISSUER
    }
    payload.update(kwargs)

    return jwt.encode(payload, key=key, algorithm=algorithm, headers=headers, json_encoder=json_encoder)


def encode2str(key=JWT_SECRET_KEY, algorithm="HS256", headers=None, json_encoder=None, **kwargs) -> str:
    """
    生成json web token

    :param key: 签名密钥
    :param headers: token头信息
    :param json_encoder:
    :param kwargs:
    :return:
    """
    return encode(key=key, algorithm=algorithm, headers=headers, json_encoder=json_encoder, **kwargs).decode('utf-8')


def decode(token, key=JWT_SECRET_KEY, verify=True, **kwargs) -> tuple:
    """
    还原json web token

    :param token: json web token
    :param key:
    :param kwargs:
    :return:
    """
    header = jwt.get_unverified_header(
        token if isinstance(token, bytes) else token.encode('utf-8'))
    payload = jwt.decode(token, key, verify=verify, leeway=JWT_TIMEOUT_LEEWAY_TIME, **kwargs)

    return header, payload


def create_rsa_key(password: str = None,
                   bits: int = 1024,
                   key_format: ('DER', 'PEM', 'OpenSSH') = 'PEM',
                   pkcs: (1, 8) = 1) -> (bytes, bytes):
    """
    创建rsa公私钥
    @params password: 密码
    @params bits: 密钥长度
    @params key_format: 密钥格式
    @params pkcs:
    @return : 私钥，公钥
    """
    key = RSA.generate(1024)
    private_key = key.exportKey(
        format=key_format, passphrase=password, pkcs=pkcs)
    public_key = key.publickey().exportKey()
    return private_key, public_key


def encrypt(data: bytes, public_key: str) -> str:
    """
    rsa加密数据
    @params data: 待加密数据
    @params public_key: 公钥
    @return : 密文的base64
    """
    recipient_key = RSA.importKey(public_key)
    cipher_rsa = PKCS1_v1_5.new(recipient_key)
    return base64.b64encode(cipher_rsa.encrypt(data))


def decrypt(data: str, private_key: str, password: str = None) -> bytes:
    """
    rsa解密数据
    @params data: 密文的base64
    @params private_key: 秘钥
    @params password: 密码
    @return : 明文
    """
    priv_key = RSA.importKey(private_key, passphrase=password)
    cipher_rsa = PKCS1_v1_5.new(priv_key)
    return cipher_rsa.decrypt(base64.b64decode(data), None)


def rsa_sign(data: bytes, private_key: str, password: str = None) -> str:
    """
    rsa签名
    @params data: 待签名数据
    @password: 签名密码
    @return : 签名
    """
    priv_key = RSA.importKey(private_key, passphrase=password)
    hash_obj = SHA256.new(data)
    signature = base64.b64encode(SignPKCS1_v1_5.new(priv_key).sign(hash_obj))
    return signature


def rsa_verify(data: str, public_key: str, signature: str) -> bool:
    """
    rsa验证签名
    @params data: 签名内容
    @params public_key: 公钥
    @params signature: 签名
    @return : 签名是否合法 True,合法   False非法
    """
    pub_key = RSA.importKey(public_key)
    hash_obj = SHA256.new(data)
    try:
        # 因为签名被base64编码，所以这里先解码，再验签
        SignPKCS1_v1_5.new(pub_key).verify(
            hash_obj, base64.b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False


if __name__ == '__main__':
    priv_key, pub_key = create_rsa_key()
    priv_key = priv_key.decode('utf8')
    pub_key = pub_key.decode('utf8')
    enc_data = encrypt(b'123456abc', pub_key)
    print(decrypt(enc_data, priv_key))
    sign = rsa_sign(b'123456abd', priv_key)
    print(rsa_verify(b'123456abd', pub_key, sign))
