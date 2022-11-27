# -*- coding: utf-8 -*-
# @FILE    : __init__.py
# @AUTH    : model_creater

# import router
# router.include_router(prefix="/{name}", router=router)

from fastapi import APIRouter

# 本模块方法
from .user import router as user_router
from .user_auth import router as user_auth_router

from .auth import router as auth_router

router = APIRouter(prefix="/system", tags=["system"])

router.include_router(prefix="/user", router=user_router)
router.include_router(prefix="/user_auth", router=user_auth_router)

router.include_router(prefix="/auth", router=auth_router)
