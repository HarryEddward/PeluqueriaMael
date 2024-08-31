from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable
from bson import ObjectId
from crud.mongodb.users.find import FindUser, FindSecretJWTID
from crud.mongodb.users.update import UpdateUser
from services.auth import JWToken
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt
from Backend.microservices.app.API.v1.logging_config import logger


class RestrictedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        logger.info('Entra en el middleware')
        logger.info(request.url.path)
        #/api/app/api/v1/client/restricted/user/delete
        if request.url.path.startswith("/api/app/api/v1/client/restricted/"):

            #logger.info(f"PATH: {request.url.path}")
            if request.method == "POST":
                logger.info("Es tipo post!")
                try:
                    body = await request.json()
                    token_id = body["token_id"]
                    token_data = body["token_data"]
                    logger.info(token_id)
                    logger.info(token_data)


                    token_id_check = JWToken.check(token_id) # Clave JWT Global
                    #print(token_id_check)
                    if token_id_check["status"] == "ok":
                        
                        #print('->',token_id_check["data"]["info"])
                        
                        user_id = token_id_check["data"]["info"]

                        

                        #Si el token_id esta correcto, irá a buscar el usuario en el db
                        secret = FindUser.secret_jwt(
                            FindSecretJWTID(
                                id=token_id_check["data"]["info"]
                            )
                        )
                        

                        #Si encontro el secreto en el usuario y todo salio bien
                        if secret.response["status"] == 'ok':
                            
                            #print('entro')
                            #Teniendo el secreto descifraremos el segundo token con la clave privada secreta que tiene el mismo usuario
                            user_secret = secret.response["data"]
                            #print('')

                            token_data_check = JWToken.check(token_data, user_secret)
                            #print('->', token_data_check)
                            
                            
                            if token_data_check["status"] == 'ok':
                                
                                #print(token_data_check)
                                email = token_data_check["data"]["info"]["email"]
                                password = token_data_check["data"]["info"]["password"]
                                
                                #print('here!')
                                renew_secret = UpdateUser.secret_jwt({
                                    "email": email,
                                    "password": password,
                                })
                                #print('final ->>>>')
                                #Intenta modificar la clave secreta del usuario 
                                if renew_secret.response["status"] == 'ok':

                                    new_token = renew_secret.response["data"]["token"]
                                    request.state.new_token = str(new_token)
                                    request.state.email = str(email)
                                    request.state.password = str(password)
                                    request.state.user_id = str(user_id)

                                    logger.info(f'new_token: {request.state.new_token}')
                                else:
                                    return JSONResponse(renew_secret.response, 401)

                            else:
                                return JSONResponse({
                                    "more": token_data_check,
                                    "type_token": "token_data"
                                }, 401)

                        else:
                            return JSONResponse(secret.response, 401)
                        

                    else:
                        return JSONResponse({
                            "info": token_id_check["info"],
                            "status": token_id_check["status"],
                            "type": token_id_check["type"],
                            "type_token": "token_id"
                        }, 401)
                    

                except Exception as e:
                    return JSONResponse({
                        "info": f"Hubo un error inesperado: {e}",
                        "status": "no",
                        "type": "UNKNOW_ERROR"
                    }, status_code=401)
            elif request.method == "OPTIONS":
                pass
            else:
                return JSONResponse({
                    "info": "En las rutas: /app/api/v1/client/restricted/, solo esta permitido el método: POST",
                    "status": "no",
                    "type": "INVALID_METHOD"
                })
        return await call_next(request)       
