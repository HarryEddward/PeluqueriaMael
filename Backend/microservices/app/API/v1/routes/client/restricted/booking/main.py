from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/booking")



@router.post("/do")
async def root(request: Request):
    
    data: dict = {
        "info": {
            "email": request.state.email,
            "password": request.state.password
        }
    }

    return {
        'hello': ':)'
    }