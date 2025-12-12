from fastapi import APIRouter

# 本模块方法
from .password_lock.api import router as password_lock_router
from .system.api import router as system_router
from .system.api.oauth import oauth_router
from .upload.api import router as upload_router
from .wechat.api import router as wechat_router

api_router = APIRouter(prefix="/api", tags=["api"])

api_router.include_router(router=oauth_router)
api_router.include_router(router=system_router)
api_router.include_router(router=password_lock_router)
api_router.include_router(router=wechat_router)
api_router.include_router(router=upload_router)
