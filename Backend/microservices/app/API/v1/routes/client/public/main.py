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
from routes.client.schemes.general import schemes
from services.auth import JWToken
from crud.mongodb.users.add import AddUser
from crud.mongodb.users.validation import ValidationUser
from crud.mongodb.users.update import UpdateUser
from crud.mongodb.users.find import FindUser, FindSecretJWTID, Find
'''from Backend.microservices.app.API.v1.routes.client.public.responses import (
    responses_login,
)'''

router = APIRouter(prefix="/public")


#Union[Credentials, Token]

@router.options('/login')
async def Loggin_User_Options(response: Response):

    response.headers["Allow"] = "POST, OPTIONS"
    response.headers["Content-Type"] = "text/plain"
    return "POST, OPTIONS"

@router.post('/login')
async def Loggin_User(request: Request, raw_data: schemes.Credentials):

    try:
        data = raw_data.model_dump()

        # Busca si el usuario ya existe en la base de datos
        existing_user = FindUser.info(Find(email=data["email"]))
        
        if existing_user.response["type"] == 'NO_FOUND_USER':
            # Si el usuario ya existe, devuelve un error de usuario existente
            return JSONResponse(existing_user.response, 400)
        
        # Valida al usuario recién agregado
        validation_response = ValidationUser({
            "email": data["email"],
            "password": data["password"],
            "info": False
        })
        print('validation ->', validation_response.response)

        if validation_response.response["status"] != "ok":
            # Si no se pudo validar al usuario, devuelve un error
            return JSONResponse(validation_response.response, 400)

        # Actualiza el secreto JWT del usuario
        secret_response = UpdateUser.secret_jwt({
            "email": data["email"],
            "password": data["password"],
        })
        print('aqui bro ->', secret_response.response)

        
        if secret_response.response["status"] != 'ok':
            print('pasa por aqui bro')
            # Si no se pudo actualizar el secreto JWT, devuelve un error
            return JSONResponse(secret_response.response, 400)

        # Crea el token JWT para el usuario
        token_id_response = JWToken.create(validation_response.response["data"])
        #print('oooo->', token_id_response)

        if token_id_response["status"] != 'ok':
            # Si no se pudo crear el token JWT, devuelve un error
            return JSONResponse(token_id_response, 400)

        print('<->',token_id_response["token"])
        print('<->', secret_response.response["data"]["token"])
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

@router.post('/register')
async def Register_User(request: Request, raw_data: schemes.Credentials):
    '''
    Registra un nuevo usuario.
    '''
    try:
        data = raw_data.model_dump()
        
        # Busca si el usuario ya existe en la base de datos
        existing_user = FindUser.info(Find(email=data["email"]))
        
        if existing_user.response["type"] == 'FOUND_USER':
            # Si el usuario ya existe, devuelve un error de usuario existente
            return JSONResponse(existing_user.response, 409)
        
        # Agrega el usuario a la base de datos
        add_user_response = AddUser({
            "email": data["email"],
            "password": data["password"]
        })
        
        print(add_user_response.response)

        if add_user_response.response["status"] != 'ok':
            # Si no se pudo agregar el usuario, devuelve un error
            return JSONResponse(add_user_response.response, 400)
        
        # Valida al usuario recién agregado
        validation_response = ValidationUser({
            "email": data["email"],
            "password": data["password"],
            "info": False
        })

        print('ValidationUser->', validation_response.response)

        if validation_response.response["status"] != "ok":
            # Si no se pudo validar al usuario, devuelve un error
            print('pasa por dentro?')
            return JSONResponse(validation_response.response, 400)

        # Actualiza el secreto JWT del usuario
        secret_response = UpdateUser.secret_jwt({
            "email": data["email"],
            "password": data["password"],
        })
        print('secret_response ->', secret_response.response)
        
        if secret_response.response["status"] != 'ok':
            # Si no se pudo actualizar el secreto JWT, devuelve un error
            print('Esta bien?: ', secret_response.response["status"])
            return JSONResponse(secret_response.response, 400)
        
        print('pasa por aqui?')

        # Crea el token JWT para el usuario
        token_id_response = JWToken.create(validation_response.response["data"])
        print('token_id_response ->', token_id_response)

        if token_id_response["status"] != 'ok':
            # Si no se pudo crear el token JWT, devuelve un error
            return JSONResponse(token_id_response, 400)

        print('acaba respondiendo con un estatus positivo')
        # Devuelve la respuesta exitosa con los tokens generados
        return JSONResponse({
            "token_id": token_id_response["token"],
            "token_data": secret_response.response["data"]["token"]
        }, 200)
    
    except Exception as e:
        # Maneja cualquier error desconocido
        return JSONResponse({
            "info": "Error desconocido por el servidor",
            "status": "no",
            "type": "UNKNOWN_ERROR",
            "detail": str(e)
        }, 500)
