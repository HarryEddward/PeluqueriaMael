from fastapi import APIRouter


from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)

from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Union




import json
#Schemes
from API.schemes.public import *

#JWT
from API.functionalities.auth import JWToken


router = APIRouter()



@router.post('/login')
async def root(data: Union[Credentials, Token]):
    try:
        if isinstance(data, Token):
            token_info = JWToken.check(data.token)
            if token_info["status"] == "ok":
                user = coleccion.find_one({
                    'number_phone': token_info["payload"]["number_phone"],
                    'password': token_info["payload"]["password"],
                })
                if user:
                    return JSONResponse(
                        content={
                            "info": 'Se validó correctamente el usuario mediante JWT',
                            "user": token_info["payload"],
                            "STAT": 'success',
                            'valid': 1
                        },
                        status_code=200
                    )
                else:
                    return JSONResponse(
                        content={
                            "info": "Usuario no encontrado",
                            "STAT": "error"
                        },
                        status_code=404
                    )
            else:
                return JSONResponse(
                    content={
                        "info": "Token JWT inválido. No se pudo decodificar.",
                        "status": "no",
                        "type": "JWT_CODIFY_ERROR"
                    },
                    status_code=401
                )
        else:
            return JSONResponse(
                content={
                    "info": "Datos de autenticación incorrectos",
                    "status": "error",
                    "type": "INVALID_AUTH_DATA"
                },
                status_code=400
            )
    except Exception as e:
        return JSONResponse(
            content={
                "info": "Error interno del servidor",
                "status": "error",
                "type": "INTERNAL_SERVER_ERROR"
            },
            status_code=500
        )


@router.post('/register')
async def root(data: Union[NewUser, Token]):

    '''
    En register primero validara si el ususario existe
    si no existe creara el usuario, asi añadire el token
    y lo redirigira

    Validara si tienen el mismo email tambien esta replicado
    '''
    try:
    
    
        if isinstance(data, Token):
            token = validate_token(data.token)

            if token["valid"] == 1:
                return JSONResponse(
                    content={
                        "info": "El token se descifro",
                        "token": token["token"],
                        "STAT": "success"
                    },
                    status_code=200
                )
            else:
                return JSONResponse(
                    content={
                        "info": token["info"],
                        "STAT": token["STAT"]
                    },
                    status_code=404
                )

        elif isinstance(data, NewUser):

            username = data.user
            password = data.psw
            email = data.email


            existing_user = coleccion.find_one({
                "$or": [
                    {"usuario": username},
                    {"email": email},
                ]
            })

            #Si no existe el usuario
            if not existing_user:

                add_user: NewUser = {
                    "usuario": username,
                    "contraseña": password,
                    "email": email
                };

                coleccion.insert_one(add_user);
            
                token = create_token({
                    "user": username,
                    "psw": password,
                    "email": email
                })

                return JSONResponse(
                    content={
                        "info": "Se agrego correctamente el usuario",
                        "token": token["token"],
                        "STAT": "success"
                    },
                    status_code=200
                )
            else:
                return JSONResponse(
                    content={
                        "info": "El usuario existe",
                        "STAT": "exist"
                    },
                    status_code=409
                )
    
    except ValidationError as e:
        return JSONResponse(
            content={
                "info": f"error: {e}",
                "STAT": "invalid"
                },
                status_code=422
            )



'''
En booking
'''


@router.post('booking')
async def root( 
    
    #Extraera la informacion del token del supuesto usuario
    #Y lo validara y dara para hacer la operacion
    data: Token
    
    ):
    
    
    try:
        pass
    except ValidationError as e:
        pass
    
    pass