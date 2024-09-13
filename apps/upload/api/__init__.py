# -*- coding: utf-8 -*-
# @FILE    : __init__.py
# @AUTH    : model_creater

# import router
# router.include_router(prefix="/{name}", router=router)

from fastapi import APIRouter

# 本模块方法
from .upload import router as upload_router

router = APIRouter(prefix="/upload", tags=["upload"])

router.include_router(prefix="/upload", router=upload_router)
