# -*- coding: utf-8 -*-
# @File    : api/auth.py
# @AUTH    : code_creater

import uuid
import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends

from mysqlengine.repositories.unit_worker import UnitWorker
from web import exceptions
from web.dependencies.db import get_db, get_unit_worker
from web.dependencies.pagination import PageSchema
from web.dependencies.token import TokenSchema
from web.response import success

# 通用方法
from commons.Helpers import refresh_tokener, tokener
from commons.Helpers.Helper_JWT import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidSignatureError,
)

# 本模块方法
from ..models.user import User
from ..models.user_auth import UserAuth
from ..schemas.user import UserSchema
from ..schemas.user_auth import UserAuthSchema

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.auth")


@router.post("/refresh_token")
async def get_refresh_token(
    ttype: int = Body(..., embed=True),
    identifier: str = Body(..., embed=True),
    credential: str = Body(..., embed=True),
    unit_worker: UnitWorker = Depends(get_unit_worker),
):
    # 使用 Schema 构建查询条件
    user_auth_schema = UserAuthSchema(ttype=ttype, identifier=identifier, credential=credential)
    page_schema = PageSchema(limit=1, skip=0, use_pager=False)

    # 使用Repository搜索方法
    async with unit_worker as uw:
        user_auth_repo = uw.get_repository(UserAuth)
        result = await user_auth_repo.search(user_auth_schema, page_schema)
        user_auth_list = result["data"]

    if not user_auth_list:
        raise exceptions.Http403ForbiddenException(exceptions.Http403ForbiddenException.PasswordError, "账号信息不正确")

    user_auth = user_auth_list[0]

    # 生成jwt
    token_schema = TokenSchema(
        user_id=str(user_auth.user_id),
    )
    token = tokener.encode(**token_schema.model_dump())
    refresh_token = refresh_tokener.encode(**token_schema.model_dump())

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
        user_id = payload.get("user_id")
    except InvalidSignatureError:
        raise exceptions.Http401UnauthorizedException(
            exceptions.Http401UnauthorizedException.TokenIllegal, "token不合法"
        )
    except ExpiredSignatureError:
        raise exceptions.Http401UnauthorizedException(
            exceptions.Http401UnauthorizedException.TokenTimeout, "token已过期"
        )

    # 生成jwt
    token_schema = TokenSchema(
        user_id=str(user_id),
    )
    token = tokener.encode(**token_schema.model_dump())

    return success(
        {
            "token": token,
            "refresh_token": refresh_token,
        }
    )


@router.post("/signin")
async def create_user_auth(
    user_auth_schema: UserAuthSchema = Body(...),
    unit_worker: UnitWorker = Depends(get_unit_worker),
):
    user_schema = UserSchema(username=f"user_{str(uuid.uuid4())[:6]}")
    async with unit_worker as uw:
        user_repo = uw.get_repository(User)
        user_auth_repo = uw.get_repository(UserAuth)
        # 创建用户
        user = await user_repo.create_one(user_schema)

        # 创建用户认证信息
        user_auth_data = user_auth_schema.model_dump()
        user_auth_data["user_id"] = user.id
        user_auth_schema_with_user_id = UserAuthSchema(**user_auth_data)
        user_auth = await user_auth_repo.create_one(user_auth_schema_with_user_id)

    user_auth_response = UserAuthSchema.model_validate(user_auth)

    return success(
        {
            "data": user_auth_response.model_dump(),
        }
    )
