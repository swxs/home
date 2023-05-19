from typing import List, Optional

import pydantic
from fastapi import Header, Query
from pydantic import BaseModel

from apps.system import consts
from apps.system.dao.user_auth import UserAuth

# 通用方法
from commons.Helpers import refresh_tokener, tokener
from commons.Helpers.Helper_JWT import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidSignatureError,
)

# 本模块方法
from ..exceptions.http_401_unauthorized_exception import Http401UnauthorizedException


class TokenSchema(pydantic.BaseModel):
    user_id: Optional[str] = None


async def get_token(
    Authorization: str = Header(...),
):
    if not Authorization:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenLost, "token不存在")
    token = Authorization[7:]
    try:
        header, payload = tokener.decode(token)
    except (InvalidSignatureError, DecodeError):
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenIllegal, "token不合法")
    except ExpiredSignatureError:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenTimeout, "token已过期")
    return TokenSchema(**payload)


async def get_token_by_openid(
    openid: Optional[str] = Query(None),
):
    if openid:
        user_auth = await UserAuth.find_one(
            finds={
                "ttype": consts.USER_AUTH_TTYPE_WECHAT,
                "identifier": openid,
                "ifverified": consts.USER_AUTH_IFVERIFIED_TRUE,
            },
        )
        if user_auth:
            return TokenSchema(user_id=str(user_auth.user_id))
        else:
            return TokenSchema(user_id=None)
    else:
        return TokenSchema(user_id=None)
