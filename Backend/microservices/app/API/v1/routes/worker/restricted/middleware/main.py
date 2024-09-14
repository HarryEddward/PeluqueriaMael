from fastapi import APIRouter, Request, Response
from Backend.microservices.app.API.v1.routes.worker.restricted.middleware.APIWS.main import router as router_apiws
router = APIRouter(prefix="/middleware")

router.include_router(router_apiws)