
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)
from fastapi.responses import JSONResponse
from routes.client.restricted.booking.main import router as router_booking
from routes.client.restricted.data.main import router as router_data
from routes.client.restricted.user.main import router as router_user
from pydantic import BaseModel

router = APIRouter(prefix="/restricted")

router.include_router(router_data)
router.include_router(router_booking)
router.include_router(router_user)

'''
@router.post('/status')
async def root(request: Request):


    data: dict = {
        "email": request.state.email,
        "password": request.state.password,
        "renew": {
            "token": request.state.new_token
        }
    }

    try:
        return {
            "email": request.state.email,
            "password": request.state.password,
            "renew": {
                "token": request.state.new_token
            }
        }
    except AttributeError as e:
        return JSONResponse({
            "info": str(e),
            "status": "no",
            "type": "ATTRIBUTE_ERROR",
            "details": "Revisar la estructura y los datos añadidos"
        }, 401)
    except Exception as e:
        return JSONResponse({
            "info": str(e),
            "status": "no",
            "type": "ATTRIBUTE_ERROR"
        }, 401)
'''