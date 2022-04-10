from fastapi import APIRouter

from .password_lock import router as password_lock_router


router = APIRouter(prefix="/password_lock", tags=["password_lock"])

router.include_router(prefix="/password_lock", router=password_lock_router)
