# -*- coding: utf-8 -*-
# @FILE    : __init__.py
# @AUTH    : model_creater

# import router
# router.include_router(prefix="/{name}", router=router)

from fastapi import APIRouter

# 本模块方法
from .message import router as message_router

router = APIRouter(prefix="/wechat", tags=["wechat"])

router.include_router(prefix="/message", router=message_router)
