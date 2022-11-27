import logging

from fastapi import Body, Path, Query, APIRouter, HTTPException
from fastapi.param_functions import Depends

from web.dependencies.pagination import get_pagination
from commons.Helpers import tokener, refresh_tokener

# 本模块方法
from ..dao.user_auth import UserAuth
from ..schemas.user import UserSchema


router = APIRouter()

logger = logging.getLogger("main.apps.user.api.user")


@router.post("/refresh_token")
async def get_refresh_token(
    ttype: int = Body(...),
    identifier: str = Body(...),
    credential: str = Body(...),
):
    user_auth = await UserAuth.find_one(
        {
            "ttype": ttype,
            "identifier": identifier,
            "credential": credential,
        }
    )
    if not user_auth:
        raise HTTPException(status_code=403, detail="用户名或密码不正确")
    # 生成jwt
    token = tokener.encode(
        user_id=str(user_auth.user_id),
    )
    refresh_token = refresh_tokener.encode(
        user_id=str(user_auth.user_id),
    )

    return {
        "code": 0,
        "data": {
            "token": token,
            "refresh_token": refresh_token,
        },
    }


@router.post("/token")
async def get_token(
    refresh_token: str = Body(...),
):
    try:
        header, payload = refresh_tokener.decode(refresh_token)
        user_id = payload.get('user_id')
    except Exception as e:
        raise e

    # 生成jwt
    token = refresh_tokener.encode(
        user_id=str(user_id),
    )

    return {
        "code": 0,
        "data": {
            "token": token,
            "refresh_token": refresh_token,
        },
    }
