# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model

# -*- coding: utf-8 -*-
# @File    : api/user_auth.py
# @AUTH    : code_creater

import logging

from fastapi import Body, Path, Query, APIRouter
from fastapi.param_functions import Depends

from web.dependencies.pagination import get_pagination

# 通用方法
from commons.Helpers import tokener, refresh_tokener

# 本模块方法
from ..dao.user_auth import UserAuth
from ..schemas.authorize import AuthorizeSchema
from ..schemas.user_auth import UserAuthSchema

router = APIRouter()

logger = logging.getLogger("main.apps.user_auth.api.auth")


@router.post("/user_auth/")
async def check_user_auth(
    self,
    user_auth_schema: UserAuthSchema = Body(...),
):
    user_auth = await UserAuth.create(user_auth_schema.dict())
    token = tokener.encode(
        user_id=str(user_auth.user_id),
    )
    refresh_token = refresh_tokener.encode(
        user_id=str(user_auth.user_id),
    )
    return {
        "user_id": user_auth.user_id,
        "id": user_auth.id,
        "ttype": user_auth.ttype,
        "identifier": user_auth.identifier,
        "ifverified": user_auth.ifverified,
        "token": token,
        "refresh_token": refresh_token,
    }


@router.post('/token/auth/')
async def get_token(
    authorize_schema: AuthorizeSchema = Body(...),
):
    user_auth = await UserAuth.find(finds=authorize_schema.dict())
    # 生成jwt
    token = tokener.encode(
        user_id=str(user_auth.user_id),
    )
    refresh_token = refresh_tokener.encode(
        user_id=str(user_auth.user_id),
    )
    return {
        "token": token,
        "refresh_token": refresh_token,
    }


@router.post('/token/refresh/')
async def refresh_token(
    refresh_token=Body(...),
):
    header, payload = refresh_tokener.decode(refresh_token)
    user_id = payload.get('user_id')
    # try:

    # except InvalidSignatureError:
    #     raise ApiException(Info.TokenIllegal, template='Invalid Token.')
    # except ExpiredSignatureError:
    #     raise ApiException(Info.TokenTimeout, template='Token expire date.')
    # except ImmatureSignatureError:
    #     raise ApiException(Info.TokenIllegal, template='Immature signature.')
    # except Exception as e:
    #     raise ApiUnknowException(e, Info.Base)
    # 生成jwt
    token = refresh_tokener.encode(
        user_id=str(user_id),
    )
    return {
        "token": token,
        "refresh_token": refresh_token,
    }
