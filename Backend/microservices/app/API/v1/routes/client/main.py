from fastapi import APIRouter
from fastapi.responses import JSONResponse
from routes.client.restricted.main import router as router_restricted
from routes.client.public.main import router as router_public

router = APIRouter()
router.include_router(router_restricted)
router.include_router(router_public)

@router.get('/status')
async def root():

    try:
        return JSONResponse({
            "schemaVersion": 1,
            "label": "status",
            "message": "ok",
            "color": "green"
        }, 200)
    except Exception as e:
        pass