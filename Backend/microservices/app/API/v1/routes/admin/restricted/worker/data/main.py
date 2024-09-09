from fastapi import APIRouter, Response, Request

router = APIRouter(prefix="/data")


@router.options('/users')
async def Change_Workers_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/users")
async def Change_Workers():

    return 'change_personal'