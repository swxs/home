# -*- coding: utf-8 -*-
# @FILE    : __init__.py
# @AUTH    : model_creater

# import router
# router.include_router(prefix="/{name}", router=router)

from fastapi import APIRouter

# 本模块方法
from .password_lock import router as password_lock_router

router = APIRouter(prefix="/password_lock", tags=["password_lock"])

router.include_router(prefix="/password_lock", router=password_lock_router)
