from fastapi import APIRouter, Request, Response
from Backend.microservices.app.API.v1.routes.worker.restricted.main import router as router_restricted
from Backend.microservices.app.API.v1.routes.worker.public.main import router as router_public
router = APIRouter()

router.include_router(router_restricted)
router.include_router(router_public)