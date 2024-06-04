from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

def verify_cryptoapi() -> None:
    pass

@router.get('/shields.io')
async def root():

    return JSONResponse({
        'msg': 'ok'
    }, 200)