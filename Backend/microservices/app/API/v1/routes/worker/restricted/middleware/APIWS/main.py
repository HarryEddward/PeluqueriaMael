from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/apiws")


@router.options('/user')
async def User_Data_For_APIWS(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post("/user")
async def User_Data_For_APIWS(request: Request):
    
    def code():
        user_id: str = request.state.user_id

        return Response({
            "user_id": user_id,
            "status": "ok",
            "type": "SUCCESS"
        }, 200)

    def Response(res: dict, status: int) -> JSONResponse:
        res["renew"] = {
            "token": request.state.new_token
        }
        return JSONResponse(res, status)
        
    return code()