
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/restricted")


@router.post('/status')
async def root(request: Request):

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