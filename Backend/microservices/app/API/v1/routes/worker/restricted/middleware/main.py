from fastapi import APIRouter, Request, Response
from .APIWS.main import router as router_apiws
router = APIRouter(prefix="/middleware")

router.include_router(router_apiws)