from fastapi import APIRouter, Request, Response
from Backend.microservices.app.API.v1.db.redis_db.database import rate_limit

router = APIRouter(prefix="/user")



@router.options('/register')
async def Register_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/register")
@rate_limit('5/10s')
async def Register_Worker_User():

    return 'change_personal'


@router.options('/delete')
async def Delete_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/delete")
@rate_limit('5/10s')
async def Delete_Worker_User():

    return 'change_personal'

