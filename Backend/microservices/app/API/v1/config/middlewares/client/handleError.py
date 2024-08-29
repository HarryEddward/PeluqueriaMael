# handleMiddleware.py

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Puedes personalizar el manejo de errores aquí
            return JSONResponse(
                status_code=500,
                content={"message": "Ha ocurrido un error interno en el servidor."}
            )
