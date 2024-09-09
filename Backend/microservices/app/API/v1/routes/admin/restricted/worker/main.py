from fastapi import APIRouter, Request, Response
from .user.main import router as router_user

router = APIRouter(prefix="/worker")
router.include_router(router_user)


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