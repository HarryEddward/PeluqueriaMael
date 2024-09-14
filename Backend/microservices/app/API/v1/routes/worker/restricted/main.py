from fastapi import APIRouter, Request, Response
from Backend.microservices.app.API.v1.routes.worker.restricted.client.main import router as router_client
from Backend.microservices.app.API.v1.routes.worker.restricted.middleware.main import router as router_middleware
router = APIRouter(prefix="/restricted")

router.include_router(router_client)