from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Backend.microservices.app.config import net
import requests

router = APIRouter()

host = net['host']
port = net['api']['port']
protocol = net['api']['protocol']

@router.get('/shields.io')
async def root():

    try:
        #Ex.: https://localhost:8000
        link = f'{protocol}://{host}:{port}'


        print(link + '/app/v1/client/status')

        headers = {

        }
        res = requests.get(link + '/app/v1/client/status', headers=headers, verify=False)
        
        print(res)
        match res.status_code:
            case 200:
                return JSONResponse({
                    "schemaVersion": 1,
                    "label": "status",
                    "message": "ok",
                    "color": "green"
                }, 200)
                
            case _:
                return JSONResponse({
                    "schemaVersion": 1,
                    "label": "status",
                    "message": "no",
                    "color": "red"
                }, 200)
                
    except Exception as e:
        return JSONResponse({

        }, 500)

    