from fastapi import APIRouter, Request, Response
from .restricted.main import router as router_restricted
from .public.main import router as router_public
router = APIRouter()

router.include_router(router_restricted)
router.include_router(router_public)