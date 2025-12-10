# -*- coding: utf-8 -*-
# @File    : api/searcher.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends

from web.dependencies.db import get_unit_worker
from web.dependencies.unit_worker import UnitWorker
from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..models.user import User
from ..models.user_auth import UserAuth
from ..repositories.user_auth_repository import UserAuthRepository
from ..repositories.user_repository import UserRepository
from ..schemas.response import UserWithAuthSearchResponse
from ..schemas.user import UserSchema, get_user_schema
from ..schemas.user_auth import UserAuthSchema

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.searcher")


@router.get("/self", response_model=SuccessResponse[UserWithAuthSearchResponse])
async def get_user_with_user_auth_list(
    token_schema: TokenSchema = Depends(get_token),
    user_schema: UserSchema = Depends(get_user_schema),
    page_schema: PageSchema = Depends(get_pagination),
    unit_worker: UnitWorker = Depends(get_unit_worker),
):
    async with unit_worker as uw:
        user_repo: UserRepository = uw.get_repository(User)
        user_auth_repo: UserAuthRepository = uw.get_repository(UserAuth)

        # 使用Repository搜索方法
        result = await user_repo.search(user_schema, page_schema)
        user_list = result["data"]

        # 获取用户ID列表
        user_ids = [str(user.id) for user in user_list]

        # 使用Repository查找UserAuth
        if user_ids:
            user_auth_list = await user_auth_repo.find_by_user_ids(user_ids)
        else:
            user_auth_list = []

        # 构建用户认证信息字典
        infos = {
            str(user_auth.user_id): {"user_auth": UserAuthSchema.model_validate(user_auth).model_dump()}
            for user_auth in user_auth_list
        }

        # 转换为 Schema 并合并用户和认证信息
        user_data_list = []
        for user in user_list:
            user_data = UserSchema.model_validate(user).model_dump()
            user_data.update(infos.get(str(user.id), {}))
            user_data_list.append(user_data)

    return success(
        {
            "data": user_data_list,
            "pagination": result["pagination"].model_dump(),
        }
    )
