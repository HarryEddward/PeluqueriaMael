from fastapi import APIRouter, Request, Response
router = APIRouter(prefix="/public")



@router.options('/login')
async def Login_Worker_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }


@router.post("/login")
async def Login_Worker():
    pass

