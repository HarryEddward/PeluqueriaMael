from fastapi import APIRouter, Response, Request

router = APIRouter(prefix="/booking_day")

@router.options('/edit_hours_specific_day_of_the_week')
async def Add_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/edit_hours_specific_day_of_the_week")
async def Add_Worker_User():

    return 'change_personal'