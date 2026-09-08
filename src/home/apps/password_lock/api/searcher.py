# -*- coding: utf-8 -*-
# @File    : api/searcher.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Path
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.types import objectId
from home.web.schemas.pagination import PageSchema, get_pagination
from home.web.schemas.response import SuccessResponse
from home.web.schemas.search import SearchSchema, get_search
from home.web.schemas.token import get_required_user_id

# 本模块方法
from ..schemas.password_lock import PasswordLockFilter, get_password_lock_filter
from ..schemas.response import PasswordLockSearchResponse, PasswordResponse
from ..services.password_lock_service import (
    PasswordLockService,
    get_password_lock_service,
)

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.searcher")


@router.get("/self", response_model=SuccessResponse[PasswordLockSearchResponse])
async def list_self_password_locks(
    user_id: objectId = Depends(get_required_user_id),
    filter_schema: PasswordLockFilter = Depends(get_password_lock_filter),
    search_schema: SearchSchema = Depends(get_search),
    page_schema: PageSchema = Depends(get_pagination),
    service: PasswordLockService = Depends(get_password_lock_service),
):
    result = await service.search_self(
        filter_schema,
        page_schema,
        user_id=user_id,
        name_search=search_schema.search if search_schema.search else None,
    )
    return success(result)


@router.get("/self/{password_lock_id}", response_model=SuccessResponse[PasswordResponse])
async def get_self_password(
    user_id: objectId = Depends(get_required_user_id),
    password_lock_id: objectId = Path(...),
    service: PasswordLockService = Depends(get_password_lock_service),
):
    password = await service.reveal_password(password_lock_id, user_id)
    return success({"password": password})
