from fastapi import APIRouter

# 本模块方法
from .system.api import router as system_router
from .password_lock.api import router as password_lock_router

api_router = APIRouter(prefix="/api", tags=["api"])

api_router.include_router(router=password_lock_router)
api_router.include_router(router=system_router)
