# -*- coding: utf-8 -*-
# @File    : api/searcher.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.pagination import PageSchema, get_pagination
from home.web.schemas.response import SuccessResponse
from home.web.schemas.types import objectId
from home.web.schemas.token import get_required_user_id

# 本模块方法
from ..schemas.response import UserWithAuthSearchResponse
from ..schemas.user import UserFilter, get_user_filter
from ..services.user_searcher_service import (
    UserSearcherService,
    get_user_searcher_service,
)

router = APIRouter()

logger = logging.getLogger("main.apps.system.api.searcher")


@router.get("/self", response_model=SuccessResponse[UserWithAuthSearchResponse])
async def get_user_with_user_auth_list(
    _user_id: objectId = Depends(get_required_user_id),
    user_schema: UserFilter = Depends(get_user_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: UserSearcherService = Depends(get_user_searcher_service),
):
    result = await service.list_self(user_schema, page_schema)
    return success(result)
