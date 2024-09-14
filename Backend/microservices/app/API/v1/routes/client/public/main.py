from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)
from fastapi.responses import JSONResponse, Response
from pydantic import ValidationError
from typing import Union
import ujson
from Backend.microservices.app.API.v1.routes.client.schemes.general import schemes
from Backend.microservices.app.API.v1.services.auth import JWToken
from Backend.microservices.app.API.v1.crud.mongodb.client.users.add import AddUser
from Backend.microservices.app.API.v1.crud.mongodb.client.users.validation import ValidationUser
from Backend.microservices.app.API.v1.crud.mongodb.client.users.update import UpdateUser
from Backend.microservices.app.API.v1.crud.mongodb.client.users.find import FindUser, FindSecretJWTID, Find
from Backend.microservices.app.API.v1.db.redis_db.database import rate_limit
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt
from Backend.microservices.app.API.v1.logging_config import logger

router = APIRouter(prefix="/public")


#Union[Credentials, Token]

@router.options('/login')
async def Loggin_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }

@router.post('/login')
@rate_limit("0.3/seconds")
async def Loggin_User(request: Request, raw_data: schemes.Credentials):

    try:
        data: dict = raw_data.model_dump()

        email: str = data["email"]
        password: str = data["password"]

        # Busca si el usuario ya existe en la base de datos
        existing_user = FindUser.info(Find(email=email))
        
        if existing_user.response["type"] == 'NO_FOUND_USER':
            # Si el usuario ya existe, devuelve un error de usuario existente
            return JSONResponse(existing_user.response, 400)
        
        # Valida al usuario recién agregado
        validation_response = ValidationUser({
            "email": email,
            "password": password,
            "info": False
        })
        #print('validation ->', validation_response.response)

        if validation_response.response["status"] != "ok":
            # Si no se pudo validar al usuario, devuelve un error
            return JSONResponse(validation_response.response, 400)

        # Actualiza el secreto JWT del usuario
        secret_response = UpdateUser.secret_jwt({
            "email": email,
            "password": password,
        })
        #print('aqui bro ->', secret_response.response)

        
        if secret_response.response["status"] != 'ok':
            #print('pasa por aqui bro')
            # Si no se pudo actualizar el secreto JWT, devuelve un error
            return JSONResponse(secret_response.response, 400)

        user_id: str = validation_response.response["data"]
        encrypted_user_id: str = encrypt(user_id)

        # Crea el token JWT para el usuario
        token_id_response = JWToken.create(encrypted_user_id)
        #print('oooo->', token_id_response)

        if token_id_response["status"] != 'ok':
            # Si no se pudo crear el token JWT, devuelve un error
            return JSONResponse(token_id_response, 400)

        #print('<->',token_id_response["token"])
        #print('<->', secret_response.response["data"]["token"])
        # Devuelve la respuesta exitosa con los tokens generados
        return JSONResponse({
            "token_id": token_id_response["token"],
            "token_data": secret_response.response["data"]["token"]
        }, 200)

    except Exception as e:
        return JSONResponse({
            "info": "Error desconocido por el servidor",
            "status": "no",
            "type": "UNKNOW_ERROR",
            "detail": str(e)
        }, 500)


@router.options('/register')
async def Register_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "application/json"
    return {
        "options": ["POST", "OPTIONS"]
    }


@router.post('/register')
@rate_limit("15/minute")
async def Register_User(request: Request, raw_data: schemes.Credentials):
    '''
    Registra un nuevo usuario.
    *E/D (Encryption/Decryption enabled)
    '''
    try:
        data = raw_data.model_dump()

        email: str = data["email"]
        password: str = data["password"]
        
        #logger.info("Extraccion de validacion de datos hecho")

        # Busca si el usuario ya existe en la base de datos (E/D)
        existing_user = FindUser.info(Find(email=email))
        
        #logger.info("Busqueda del usuario en la base de datos hecha")

        if existing_user.response["type"] == 'FOUND_USER':
            # Si el usuario ya existe, devuelve un error de usuario existente
            return JSONResponse(existing_user.response, 409)
        
        logger.info("Email: %s", data["email"])
        # Agrega el usuario a la base de datos (E/D)
        add_user_response = AddUser({
            "email": email,
            "password": password
        })

        #logger.info("Usuario agregado en la base de datos hecha")
        
        #print(add_user_response.response)

        if add_user_response.response["status"] != 'ok':
            # Si no se pudo agregar el usuario, devuelve un error
            return JSONResponse(add_user_response.response, 400)
        
        # Valida al usuario recién agregado y devuelve _id del usuario (E/D)
        validation_response = ValidationUser({
            "email": email,
            "password": password,
            "info": False
        })

        #logger.info("Valida el usuario recien agregado")

        #print('ValidationUser->', validation_response.response)

        if validation_response.response["status"] != "ok":
            # Si no se pudo validar al usuario, devuelve un error
            #print('pasa por dentro?')
            return JSONResponse(validation_response.response, 400)

        # Actualiza el secreto JWT del usuario (E/D)
        secret_response = UpdateUser.secret_jwt({
            "email": email,
            "password": password,
        })
        #print('secret_response ->', secret_response.response)
        
        if secret_response.response["status"] != 'ok':
            # Si no se pudo actualizar el secreto JWT, devuelve un error
            #print('Esta bien?: ', secret_response.response["status"])
            return JSONResponse(secret_response.response, 400)
        
        #print('pasa por aqui?')
        #logger.info("Actualiza el secreto del usuario")

        user_id: str = validation_response.response["data"]
        #logger.info("validation_response.response[data]: %s", user_id)
        encrypted_user_id: str = encrypt(user_id)

        #.......................................................
        # Crea el token JWT para el usuario
        token_id_response = JWToken.create(encrypted_user_id)
        #print('token_id_response ->', token_id_response)
        #.......................................................

        if token_id_response["status"] != 'ok':
            # Si no se pudo crear el token JWT, devuelve un error
            return JSONResponse(token_id_response, 400)

        #print('acaba respondiendo con un estatus positivo')
        # Devuelve la respuesta exitosa con los tokens generados
        return JSONResponse({
            "token_id": token_id_response["token"],
            "token_data": secret_response.response["data"]["token"]
        }, 200)
    
    except Exception as e:
        # Maneja cualquier error desconocido
        logger.error("Error Inesperado: %s", e)
        return JSONResponse({
            "info": "Error desconocido por el servidor",
            "status": "no",
            "type": "UNKNOWN_ERROR",
            "detail": str(e)
        }, 500)
