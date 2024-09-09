from fastapi import APIRouter
from routes.admin.restricted.main import router as router_restricted

router = APIRouter()
router.include_router(router_restricted)
