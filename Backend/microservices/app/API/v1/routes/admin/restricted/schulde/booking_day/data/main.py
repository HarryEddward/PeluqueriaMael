from fastapi import APIRouter, Response, Request

router = APIRouter(prefix="/data")

@router.options('/all_week')
async def Add_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/all_week")
async def Add_Worker_User():

    return 'change_personal'