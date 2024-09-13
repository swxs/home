# -*- coding: utf-8 -*-
# @FILE    : __init__.py
# @AUTH    : model_creater

# import router
# router.include_router(prefix="/{name}", router=router)

from fastapi import APIRouter

# 本模块方法
from .file_info import router as file_info_router
from .upload import router as upload_router

router = APIRouter(prefix="/upload", tags=["upload"])

router.include_router(prefix="/file_info", router=file_info_router)
router.include_router(prefix="/upload", router=upload_router)
