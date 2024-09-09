from fastapi import APIRouter, Request, Response

router = APIRouter(prefix="/user")



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


@router.options('/remove')
async def Add_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/remove")
async def Add_Worker_User():

    return 'change_personal'



@router.options('/update')
async def Add_Worker_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/update")
async def Add_Worker_User():

    return 'change_personal'