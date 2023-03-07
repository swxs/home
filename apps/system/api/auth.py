import uuid
import logging

from fastapi import Body, Path, Query, APIRouter, HTTPException
from fastapi.param_functions import Depends

from web.response import success
from web.dependencies.token import TokenSchema
from web.exceptions.http_403_forbidden_exception import Http403ForbiddenException
from web.exceptions.http_401_unauthorized_exception import Http401UnauthorizedException

# 通用方法
from commons.Helpers import tokener, refresh_tokener
from commons.Helpers.Helper_JWT import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    ImmatureSignatureError,
)

# 本模块方法
from ..dao.user import User
from ..schemas.user import UserSchema
from ..dao.user_auth import UserAuth
from ..schemas.user_auth import UserAuthSchema

router = APIRouter()

logger = logging.getLogger("main.apps.user.api.user")


@router.post("/refresh_token")
async def get_refresh_token(
    ttype: int = Body(..., embed=True),
    identifier: str = Body(..., embed=True),
    credential: str = Body(..., embed=True),
):
    user_auth = await UserAuth.find_one(
        {
            "ttype": ttype,
            "identifier": identifier,
            "credential": credential,
        }
    )
    if not user_auth:
        raise Http403ForbiddenException(Http403ForbiddenException.PasswordError, "用户名或密码不正确")
    # 生成jwt
    token_schema = TokenSchema(
        user_id=str(user_auth.user_id),
    )
    token = tokener.encode(**token_schema.dict())
    refresh_token = refresh_tokener.encode(**token_schema.dict())

    return success(
        {
            "token": token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/token")
async def get_token(
    refresh_token: str = Body(..., embed=True),
):
    try:
        header, payload = refresh_tokener.decode(refresh_token)
        user_id = payload.get('user_id')
    except InvalidSignatureError:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenIllegal, "token不合法")
    except ExpiredSignatureError:
        raise Http401UnauthorizedException(Http401UnauthorizedException.TokenTimeout, "token已过期")

    # 生成jwt
    token_schema = TokenSchema(
        user_id=str(user_id),
    )
    token = refresh_tokener.encode(**token_schema.dict())

    return success(
        {
            "token": token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/signin")
async def create_user_auth(
    user_auth_schema: UserAuthSchema = Body(...),
):
    user = await User.create(
        params=UserSchema(
            username=f"user_{uuid.uuid4()}",
        ).dict()
    )
    user_auth_schema.user_id = user.id
    user_auth = await UserAuth.create(
        params=user_auth_schema.dict(),
    )
    return success(
        {
            "data": user_auth,
        }
    )
