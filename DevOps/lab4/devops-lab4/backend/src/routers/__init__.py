from fastapi import APIRouter

from routers.user import router as user

router = APIRouter(prefix="/api/v1")
router.include_router(user, prefix="/users", tags=["Users"])
