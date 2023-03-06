from typing import List, Optional

import pydantic
from fastapi import Query, Header
from pydantic import BaseModel

# 通用方法
from commons.Helpers import tokener, refresh_tokener
from commons.Helpers.Helper_JWT import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    ImmatureSignatureError,
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
    except InvalidSignatureError:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenIllegal, "token不合法")
    except ExpiredSignatureError:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenTimeout, "token已过期")
    return TokenSchema(**payload)
