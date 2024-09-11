from fastapi import APIRouter
from routes.admin.restricted.main import router as router_restricted
from routes.admin.public.main import router as router_public


router = APIRouter()
router.include_router(router_restricted)
router.include_router(router_public)


