from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class TextPlainMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, skip_paths: list = None):
        super().__init__(app)
        self.skip_paths = skip_paths or []

    async def dispatch(self, request: Request, call_next):
        # Verificar si la ruta debe ser omitida
        for path in self.skip_paths:
            if request.url.path.startswith(path):
                return await call_next(request)
        
        if request.headers.get('content-type') != 'text/plain':
            return JSONResponse(content={
                "info": "Content-Type debe ser text/plain"
            }, status_code=400)
        
        # Leer y decodificar el cuerpo de la solicitud
        try:
            body = await request.body()
            request.state.decoded_body = body.decode('utf-8')
        except UnicodeDecodeError:
            raise JSONResponse(
                content={
                    "info": "No se pudo decodificar el texto. Asegúrese de que el texto esté codificado en UTF-8"
                },
                status_code=400
            )
        
        response = await call_next(request)
        return response
