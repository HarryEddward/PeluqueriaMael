from fastapi import APIRouter, Response, Request
from .config.main import router as router_config

router = APIRouter(prefix="/user")
router.include_router(router_config)
