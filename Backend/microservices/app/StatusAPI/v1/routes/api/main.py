from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from Backend.microservices.app.conversor.config.config import Config
import requests
import json
import warnings
import urllib3

# Ignorar advertencias de solicitudes HTTPS no verificadas
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)

router = APIRouter()

config = Config()
host = config['host']
port = config['API']['net']['port']
protocol = config['API']['net']['protocol']

@router.get('/shields.io')
async def root():
    try:
        # Construir el enlace
        link = f'{protocol}://{host}:{port}'
        endpoint = f'{link}/api/app/api/v1/client/status'
        
        headers = {
            "Content-Type": "application/json",
            "Origin": link
        }

        print('Endpoint:', endpoint)
        print('Headers:', headers)

        res = requests.get(endpoint, headers=headers, verify=False)

        print('Response:', res)
        print('Response JSON:', res.json() if res.content else 'No content')

        if res.status_code == 200:
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
            }, status_code=res.status_code)

    except requests.RequestException as e:
        return JSONResponse({
            "schemaVersion": 1,
            "label": "status",
            "message": "no",
            "color": "red"
        }, status_code=500)
    except Exception as e:
        print(f"Exception: {e}")
        return JSONResponse({
            "schemaVersion": 1,
            "label": "status",
            "message": "no",
            "color": "red"
        }, status_code=500)