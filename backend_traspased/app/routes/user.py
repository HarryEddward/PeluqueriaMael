#Routing
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)

from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import Union
import routes.schemes.user

import pymongo
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
base_datos = cliente["PeluqueriaMael"]
coleccion = base_datos["Users"]


#Database
#from database.db import SessionLocalUsers

#Models
'''
from database.models.user import (

)
'''
import json
#Schemes
from routes.schemes.user import *

#JWT
from utils.validation import (
    create_token,
    validate_token,
)


router = APIRouter()



@router.post('/login')
async def root(data: Union[Credentials, Token]):

    

    '''
    El login solo tendra que añadir el token
    y leugo en react y react native lo redirigira a la pagina
    y luego esa pagina valiara el token y le dara la informacion
    sino si va a esa pagina sin token adecuado le rederigira al
    login
    '''

    try:
        if isinstance(data, Token):

            raw_token = validate_token(data.token)
            

            print(raw_token)

            if raw_token["valid"] == 1:
                
                token = raw_token.token

                user = coleccion.find_one({
                    'number_phone': token["number_phone"],
                    'password': token["password"],
                })

                if user:
                    
                    '''token = create_token(
                        data.get('user'),
                        data.get('psw'),
                    )'''

                    #Si existe y coinciden el usuario pasa
                    return JSONResponse(
                        content={
                            "info": 'Se valido bien el usuario por JWT',
                            "user": token,
                            "STAT": 'success',
                            'valid': 1
                        },
                        status_code=200
                    )
                else:
                    return JSONResponse(
                        content={
                            "info": 'El password o el usuario esta mal',
                            "STAT": "wrong_auth",
                            "valid": 0
                        },
                        status_code=404
                    )

            else:
                return JSONResponse(
                    content={
                        "info": raw_token["info"],
                        "STAT": raw_token["STAT"]
                    },
                    status_code=404
                )

            
            


        elif isinstance(data, Credentials):
            username = data.user
            password = data.psw

            user = coleccion.find_one({
                'usuario': username,
                'contraseña': password,
            });

            if user:
                token = create_token({
                    "user": username,
                    "psw": password,
                })

                return JSONResponse(
                    content={
                        "info": 'Se valido bien el usuario por credenciales',
                        "token": token["token"],
                        "STAT": "success"
                    },
                    status_code=200
                )
            else:
                return JSONResponse(
                    content={
                        "info": "No existe el usuario",
                        "STAT": "inexistent"
                    },
                    status_code=404
                )

        
        else:
            #Si no existe el token
            return JSONResponse(
                content={
                    "info": "No esta el JWT, ni los datos necesarios para validar",
                    "STAT": "empty"
                },
                status_code=404
            )
    except ValidationError as e:
        # Manejar la excepción ValidationError aquí
        return JSONResponse(
            content={
                "info": f"Error de validación: {e}",
                "STAT": 0
            },
            status_code=422
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