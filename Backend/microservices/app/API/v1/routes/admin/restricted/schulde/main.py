from fastapi import APIRouter, Response, Request
from .booking_day.main import router as router_booking_day

router = APIRouter(prefix="/schulde")
router.include_router(router_booking_day)
