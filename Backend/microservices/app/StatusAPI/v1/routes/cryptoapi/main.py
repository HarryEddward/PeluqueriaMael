from fastapi import FastAPI
from fastapi.responses import JSONResponse

router = FastAPI()

def verify_cryptoapi() -> None:
    pass

@router.get('/shields.io')
async def root():

    return JSONResponse({
        'msg': 'ok'
    }, 200)