# restricted.py
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable

from services.auth import JWToken

from crud.users.validation import ValidationUser


class RestrictedMiddleware(BaseHTTPMiddleware):



    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        # Verifica si la ruta es la restringida

        request.state.custom_data = request.url.path

        '''
        La ruta restringida del cliente, siempre deberá de validar por jwt su usuario
        y siempre por el metodo post
        '''
        if request.url.path.startswith("/app/api/v1/client/restricted/"):

            if request.method == "POST":

                try:
                    token = await self.get_token(request)
                    self.validate_user(token)
                except HTTPException as e:
                    raise e
                except Exception as e:
                    raise HTTPException(status_code=401, detail="Hubo un error de validación")

                self.validate_user()

                # Si es la ruta restringida, agrega el encabezado personalizado
                response = await call_next(request)
                # Añadir el path como un encabezado en la solicitud
                return response
            else:
                HTTPException(status_code=401, detail="Solo acceso con el único método: POST")

        # Si no es la ruta restringida, continúa con la ejecución normal
        return await call_next(request)

    #Obtiene el token del request
    async def get_token(self, request: Request) -> str:
        form_data = await request.form()
        return form_data["token"]
    
    def validate_user(self, token: str):
        try:
            jwt = JWToken.check(token)

            if jwt["status"] == "ok":
                
                jwt["data"]["info"]
            else:
                JSONResponse(jwt, status_code=401)

        except Exception:
            HTTPException(status_code=401, detail="Hubo un error de validación")
