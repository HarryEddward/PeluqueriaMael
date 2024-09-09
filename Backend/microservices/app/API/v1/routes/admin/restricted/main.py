from fastapi import APIRouter
from .worker.main import router as router_worker
from .user.main import router as router_user
from .schulde.main import router as router_schulde

router = APIRouter(prefix="/restricted")
router.include_router(router_worker)
router.include_router(router_user)
router.include_router(router_schulde)
