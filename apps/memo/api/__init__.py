# -*- coding: utf-8 -*-
# @FILE    : __init__.py
# @AUTH    : model_creater

# import router
# router.include_router(prefix="/{name}", router=router)

from fastapi import APIRouter

# 本模块方法
from .todo import router as todo_router

router = APIRouter(prefix="/memo", tags=["memo"])

router.include_router(prefix="/todo", router=todo_router)
