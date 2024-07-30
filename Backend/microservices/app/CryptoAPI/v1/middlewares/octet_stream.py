from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

class OctetStreamMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, skip_paths: list = None):
        super().__init__(app)
        self.skip_paths = skip_paths or []

    async def dispatch(self, request: Request, call_next):
        # Verificar si la ruta debe ser omitida
        for path in self.skip_paths:
            if request.url.path.startswith(path):
                return await call_next(request)
        
        content_type = request.headers.get('content-type')

        if content_type not in (
            'application/octet-stream'
        ):
            return JSONResponse(content={
                "info": "Content-Type debe ser application/octet-stream"
            }, status_code=400)
        
        # Leer y decodificar el cuerpo de la solicitud
        try:
            request.state.body = await request.body()
        except UnicodeDecodeError:
            raise JSONResponse(
                content={
                    "info": "No se pudo decodificar el texto. Asegúrese de que el texto esté codificado en UTF-8"
                },
                status_code=400
            )
        
        response = await call_next(request)
        return response
