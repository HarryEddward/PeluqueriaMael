from fastapi import (
    APIRouter,
    Request
)
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post('/encrypt')
async def root(request: Request):
    # Acceder al texto decodificado desde el middleware
    texto = request.state.decoded_body

    # Validar que el contenido no esté vacío
    if not texto.strip():
        return JSONResponse(
            content={
                "info": "El contenido del texto no puede estar vacío",
                "status": "no",
                "type": "EMPTY_STRING"
            }, status_code=400
        )

    # Procesar el texto
    resultado = f"Texto recibido: {texto}"

    return {"resultado": resultado}


@router.post('/decrypt')
async def root(request: Request):
    # Acceder al texto decodificado desde el middleware
    texto = request.state.decoded_body

    # Validar que el contenido no esté vacío
    if not texto.strip():
        return JSONResponse(
            content={
                "info": "El contenido del texto no puede estar vacío",
                "status": "no",
                "type": "EMPTY_STRING"
            }, status_code=400
        )

    # Procesar el texto
    resultado = f"Texto recibido: {texto}"

    return {"resultado": resultado}