from fastapi import APIRouter, Request, Response
from Backend.microservices.app.API.v1.routes.worker.restricted.client.booking.main import router as router_booking
router = APIRouter(prefix="/client")

router.include_router(router_booking)