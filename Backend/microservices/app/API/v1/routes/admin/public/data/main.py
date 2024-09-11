from fastapi import APIRouter, Response, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/data")


@router.options('/proxy_tor_url')
async def Change_Workers_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["GET", "OPTIONS"]
    }

@router.get("/proxy_tor_url")
async def Onion_Url():
    try:
        with open("../../../../../../var/lib/tor/hidden_service/hostname") as file:
            content: str = file.read()

        return content.strip()
    except FileExistsError:
        return JSONResponse({
            "info": f"No se puedo encontrar el archivo o hubo un problema: {e}",
            "status": "no",
            "type": "ERROR_NOT_FOUND_FILE"
        }, 404)
    except Exception as e:
        return JSONResponse({
            "info": f"Hubo un error global en la ruta de: /proxy_tor_url: {e}",
            "status": "no",
            "type": "UNKNOW_ERROR"
        }, 500)