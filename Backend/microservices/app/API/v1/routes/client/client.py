from fastapi import APIRouter


from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)

from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Union
import json

#Schemes
from routes.client.schemes.general import schemes

#JWT
from services.auth import JWToken

#SubRoutes
import routes.client.restricted.main

router = APIRouter()
router.include_router(routes.client.restricted.main.router)


#Union[Credentials, Token]

@router.post('/token_id')
async def root(request: Request, data: schemes.Credentials):

    try:
        pass
    except Exception as e:
        return JSONResponse({

        }, 500)

    return {
        "info": "login"
    }