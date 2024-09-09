from fastapi import APIRouter, Response, Request
from .update.main import router as router_update
from .data.main import router as router_data

router = APIRouter(prefix="/booking_day")
router.include_router(router_update)
router.include_router(router_data)

