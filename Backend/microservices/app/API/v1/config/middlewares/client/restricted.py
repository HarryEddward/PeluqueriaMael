from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable
from bson import ObjectId

from crud.users.find import FindUser, FindSecretJWTID
from crud.users.update import UpdateUser
from services.auth import JWToken

class RestrictedMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        if request.url.path.startswith("/app/api/v1/client/restricted/"):

            print(request.method)
            if request.method == "POST":
                try:
                    body = await request.json()
                    token_id = body["token_id"]
                    token_data = body["token_data"]
                    print(token_id)
                    print(token_data)

                    

                    #request.state.token_id = body["token_id"] #1 Token
                    #request.state.token_data = body["token_data"] #2 Token

                    #print('middleware ->', token_id)
                    #print('middleware ->', token_data)

                    token_id_check = JWToken.check(token_id) # Clave JWT Global
                    print(token_id_check)
                    if token_id_check["status"] == "ok":
                        
                        print('->',token_id_check["data"]["info"])
                        
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
                            print('')

                            token_data_check = JWToken.check(token_data, user_secret)
                            print('->', token_data_check)
                            
                            
                            if token_data_check["status"] == 'ok':
                                
                                #print(token_data_check)
                                email = token_data_check["data"]["info"]["email"]
                                password = token_data_check["data"]["info"]["password"]
                                
                                #print('here!')
                                renew_secret = UpdateUser.secret_jwt({
                                    "email": email,
                                    "password": password,
                                })
                                print('final ->>>>')
                                #Intenta modificar la clave secreta del usuario 
                                if renew_secret.response["status"] == 'ok':

                                    new_token = renew_secret.response["data"]["token"]
                                    request.state.new_token = str(new_token)
                                    request.state.email = str(email)
                                    request.state.password = str(password)
                                    request.state.user_id = str(user_id)
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
                
            else:
                return JSONResponse({
                    "info": "En las rutas: /app/api/v1/client/restricted/, solo esta permitido el método: POST",
                    "status": "no",
                    "type": "INVALID_METHOD"
                })
        return await call_next(request)       
