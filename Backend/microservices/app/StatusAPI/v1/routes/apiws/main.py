from fastapi import APIRouter
from fastapi.responses import JSONResponse
from Backend.microservices.app.conversor.config.config import Config
import asyncio
import websockets

router = APIRouter()

config = Config()
host = config['host']
port = config['APIWS']['net']['port']
protocol = config['APIWS']['net']['protocol']

async def websocket_status(url: str, endpoint: str) -> JSONResponse:
    try:
        async with websockets.connect(url) as websocket:
            await websocket.send(endpoint)

            try:
                res = await asyncio.wait_for(websocket.recv(), timeout=10)

                print('res->', res)
                if res == 'ok':
                    return JSONResponse({
                        "schemaVersion": 1,
                        "label": "status",
                        "message": "ok",
                        "color": "green"
                    }, status_code=200)
                else:
                    return JSONResponse({
                        "schemaVersion": 1,
                        "label": "status",
                        "message": "no",
                        "color": "red"
                    }, status_code=500)

            except asyncio.TimeoutError:
                return JSONResponse({
                    "schemaVersion": 1,
                    "label": "status",
                    "message": "no",
                    "color": "red"
                }, status_code=500)

    except Exception as e:
        return JSONResponse({
            "schemaVersion": 1,
            "label": "status",
            "message": "no",
            "color": "red"
        }, status_code=500)


@router.get('/shields.io')
async def root():
    link = f'{protocol}://{host}:{port}'
    endpoint = 'status'
    response = await websocket_status(link, endpoint)
    return response
