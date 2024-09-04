from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from routes.client.restricted.main import router as router_restricted
from routes.client.public.main import router as router_public
from Backend.microservices.app.API.v1.db.redis_db.database import rate_limit

router = APIRouter()
router.include_router(router_restricted)
router.include_router(router_public)


@router.options('/status')
async def Status_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.get('/status')
#@rate_limit("5/10s")
async def Status():
    """AI is creating summary for Status

    Returns:
        [type]: [description]
    """
    try:
        return JSONResponse({
            "schemaVersion": 1,
            "label": "status",
            "message": "ok",
            "color": "green"
        }, 200)
    except Exception:
        return JSONResponse({
            "schemaVersion": 1,
            "label": "status",
            "message": "ok",
            "color": "green"
        }, 200)