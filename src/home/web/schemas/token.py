import logging
from typing import Optional

import pydantic
from fastapi import Header, Query, Request
from fastapi.param_functions import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from home.apps.system import consts
from home.apps.system.repositories.user_auth_repository import UserAuthRepository
from home.apps.system.schemas.user_auth import UserAuthSchema
from home.web.dependencies.session import get_session
from home.web.schemas.types import objectId, validate_object_id

# 通用方法
from home.commons.Helpers import refresh_tokener, tokener
from home.commons.Helpers.Helper_JWT import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidSignatureError,
)

# 本模块方法
from ..exceptions.http_401_unauthorized_exception import Http401UnauthorizedException

logger = logging.getLogger("main.web.schemas.token")


class TokenSchema(pydantic.BaseModel):
    user_id: Optional[objectId] = None


async def get_token(
    Authorization: str = Header(...),
):
    if not Authorization:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenLost, "token不存在")
    token = Authorization[7:]
    try:
        _, payload = tokener.decode(token)
    except (InvalidSignatureError, DecodeError) as exc:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenIllegal, "token不合法") from exc
    except ExpiredSignatureError as exc:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenTimeout, "token已过期") from exc
    return TokenSchema(**payload)


async def get_required_user_id(token_schema: TokenSchema = Depends(get_token)) -> objectId:
    """已登录用户的 user_id；缺失时 401。"""
    if token_schema.user_id is None:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenLost, "token不存在")
    return token_schema.user_id


async def get_token_by_openid(
    session: AsyncSession = Depends(get_session),
    openid: Optional[str] = Query(None),
):
    if openid:
        user_auth_repo = UserAuthRepository(session)
        user_auth = await user_auth_repo.find_one_or_none(
            UserAuthSchema(
                ttype=consts.UserAuth_Ttype.WECHAT,
                identifier=openid,
                ifverified=consts.UserAuth_Ifverified.VERIFIED,
            )
        )
        if user_auth:
            return TokenSchema(user_id=user_auth.user_id)
        return TokenSchema(user_id=None)
    return TokenSchema(user_id=None)


def _decode_user_id(token: Optional[str]) -> Optional[objectId]:
    """解码单个 token 并取出 user_id，失败返回 None（区分过期/非法并记录日志）。"""
    if not token:
        return None
    try:
        _, payload = tokener.decode(token)
        user_id = payload.get("user_id")
        if not user_id:
            return None
        return validate_object_id(user_id)
    except ExpiredSignatureError:
        logger.info("optional auth: token 已过期，按未登录处理")
        return None
    except (InvalidSignatureError, DecodeError):
        logger.warning("optional auth: token 非法，按未登录处理")
        return None
    except ValueError:
        logger.warning("optional auth: token user_id 非法，按未登录处理")
        return None


async def get_optional_user_id(request: Request) -> Optional[objectId]:
    """软登录检测：Bearer / Cookie / Query 依次解析，失败返回 None。"""
    auth_header = request.headers.get("Authorization", "")
    sources = [
        auth_header[7:] if auth_header.startswith("Bearer ") else None,
        request.cookies.get("access_token"),
        request.query_params.get("token"),
    ]
    for token in sources:
        user_id = _decode_user_id(token)
        if user_id:
            return user_id
    return None
