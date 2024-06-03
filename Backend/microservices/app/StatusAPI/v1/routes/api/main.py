from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Backend.microservices.app.config import net
import requests

router = FastAPI()

host = net['host']
port = net['api']['port']
protocol = net['api']['protocol']

@router.get('/shields.io')
async def root():

    #Ex.: https://localhost:8000
    link = f'{protocol}://{host}:{port}'

    res = requests.get(link + '/app/v1/client/status', verify=False)
    
    match res.status_code:
        case 200:
            return JSONResponse({
                "schemaVersion": 1,
                "label": "status",
                "message": "ok",
                "color": "green"
            }, 200)
            pass
        case _:
            return JSONResponse({
                "schemaVersion": 1,
                "label": "status",
                "message": "no",
                "color": "red"
            }, 200)
            pass

    