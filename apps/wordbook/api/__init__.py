# -*- coding: utf-8 -*-
# @FILE    : __init__.py
# @AUTH    : model_creater

# import router
# router.include_router(prefix="/{name}", router=router)

from fastapi import APIRouter

router = APIRouter(prefix="/wordbook", tags=["wordbook"])
