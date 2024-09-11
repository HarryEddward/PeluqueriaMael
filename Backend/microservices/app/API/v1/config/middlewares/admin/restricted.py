from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable
from crud.mongodb.client.users.find import FindUser, FindSecretJWTID
from crud.mongodb.client.users.update import UpdateUser
from services.auth import JWToken
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt
from Backend.microservices.app.API.v1.logging_config import logger


class RestrictedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        logger.info('Entra en el middleware')
        logger.info(request.url.path)

        # Solo se permite el acceso a rutas restringidas y el método POST
        if request.url.path.startswith("/api/app/api/v1/admin/restricted/"):
            if request.method != "POST":
                return JSONResponse({
                    "info": "Solo está permitido el método: POST",
                    "status": "no",
                    "type": "INVALID_METHOD"
                }, 405)

            try:
                body = await request.json()
                token_id, token_data = body["token_id"], body["token_data"]
                logger.info(f"Token_ID: {token_id}, Token_Data: {token_data}")

                # Verificación del token global
                token_id_check = JWToken.check(token_id)
                if token_id_check["status"] != "ok":
                    return JSONResponse({
                        "info": token_id_check["info"],
                        "status": token_id_check["status"],
                        "type": token_id_check["type"],
                        "type_token": "token_id"
                    }, 401)

                user_id = decrypt(token_id_check["data"]["info"])

                # Buscar el secreto del usuario en la base de datos
                secret = FindUser.secret_jwt(FindSecretJWTID(id=user_id))
                if secret.response["status"] != 'ok':
                    return JSONResponse(secret.response, 401)

                # Desencriptar y verificar el segundo token con la clave secreta del usuario
                decrypted_secret_key = decrypt(secret.response["data"])
                token_data_check = JWToken.check(token_data, decrypted_secret_key)
                if token_data_check["status"] != "ok":
                    return JSONResponse({
                        "more": token_data_check,
                        "type_token": "token_data"
                    }, 401)

                email, password = token_data_check["data"]["info"]["email"], token_data_check["data"]["info"]["password"]

                # Actualizar la clave secreta del usuario
                renew_secret = UpdateUser.secret_jwt({"email": email, "password": password})
                if renew_secret.response["status"] != 'ok':
                    return JSONResponse(renew_secret.response, 401)

                # Guardar los datos en el estado de la request
                request.state.new_token = str(renew_secret.response["data"]["token"])
                request.state.email = email
                request.state.password = password
                request.state.user_id = user_id
                logger.info(f'new_token: {request.state.new_token}')

            except Exception as e:
                return JSONResponse({
                    "info": f"Hubo un error inesperado: {e}",
                    "status": "no",
                    "type": "UNKNOWN_ERROR"
                }, 500)

        return await call_next(request)
