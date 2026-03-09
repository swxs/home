# -*- coding: utf-8 -*-

from fastapi import APIRouter

# 本模块方法
from .runs import router as runs_router
from .workflows import router as workflows_router

router = APIRouter(prefix="/workflow", tags=["workflow"])

router.include_router(prefix="/workflows", router=workflows_router)
router.include_router(prefix="/runs", router=runs_router)
