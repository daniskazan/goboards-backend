from api.v1.routing import router as v1_router
from fastapi import APIRouter

router = APIRouter(prefix="/api")

router.include_router(v1_router)
