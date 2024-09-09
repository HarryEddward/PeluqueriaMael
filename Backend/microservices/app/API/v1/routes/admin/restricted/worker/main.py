from fastapi import APIRouter, Request, Response
from .user.main import router as router_user
from .data.main import router as router_data

router = APIRouter(prefix="/worker")
router.include_router(router_user)
router.include_router(router_data)
