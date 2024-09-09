from fastapi import APIRouter, Request, Response
from .client.main import router as router_client
router = APIRouter(prefix="/restricted")

router.include_router(router_client)