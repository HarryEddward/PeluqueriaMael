from fastapi import APIRouter, Request, Response
from .booking.main import router as router_booking
router = APIRouter(prefix="/client")

router.include_router(router_booking)