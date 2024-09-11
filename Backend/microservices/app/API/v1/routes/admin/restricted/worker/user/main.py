from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from Backend.microservices.app.API.v1.db.redis_db.database import rate_limit

router = APIRouter(prefix="/user")




class StructureRegister(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None

@router.options('/register')
async def Register_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/register")
@rate_limit('5/10s')
async def Register_Worker_User(request: Request, data_raw: StructureRegister):

    def code() -> dict:
        pass

    try:
        def Response(res: dict, status: int) -> JSONResponse:
            res["renew"] = {
                "token": request.state.new_token
            }
            return JSONResponse(res, status)
        
        return code()

    except Exception as e:
        return JSONResponse({
            "info": f"Error desconocido por el servidor: {e}",
            "status": "no",
            "type": "UNKNOW_ERROR",
            "renew": {
                "token": request.state.new_token
            }
        }, 500)




class StructureDelete(BaseModel):
    token_id: Optional[str] = None
    token_data: Optional[str] = None

@router.options('/delete')
async def Delete_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/delete")
@rate_limit('5/10s')
async def Delete_Worker_User(request: Request, data_raw: StructureDelete):


    def code() -> dict:
        pass

    try:
        def Response(res: dict, status: int) -> JSONResponse:
            res["renew"] = {
                "token": request.state.new_token
            }
            return JSONResponse(res, status)
        
        return code()

    except Exception as e:
        return JSONResponse({
            "info": f"Error desconocido por el servidor: {e}",
            "status": "no",
            "type": "UNKNOW_ERROR",
            "renew": {
                "token": request.state.new_token
            }
        }, 500)

