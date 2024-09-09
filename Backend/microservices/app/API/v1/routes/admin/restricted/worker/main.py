from fastapi import APIRouter, Request, Response

router = APIRouter(prefix="/worker")

@router.options('/add')
async def Add_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/add")
async def Add_Worker_User():

    return 'change_personal'



@router.options('/change_users')
async def Change_Workers_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/change_users")
async def Change_Workers():

    return 'change_personal'