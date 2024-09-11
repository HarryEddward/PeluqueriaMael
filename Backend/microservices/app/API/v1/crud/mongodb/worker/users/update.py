from pydantic import BaseModel, EmailStr
from pydantic import ValidationError
from services.secrets_generator.main import secrets_generator
from bson import ObjectId
import numba as nb
from abc import ABC, abstractmethod

from .validation import ValidationUser
from services.auth import JWToken
from Backend.microservices.app.API.v1.db.mongodb.database import workers
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt
from Backend.microservices.app.API.v1.logging_config import logger

'''
Aquí estaran todos los métodos que se haran uso, estan de forma controlada
para que no se puedan modificar cualquier dato que nos de la gana.
Para evitar fallos de seguirdad

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjp7ImVtYWlsIjoiYWRyaWFuZWxjYXBvQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiZnVja195b3UifSwiZXhwIjoxNzE1NjI3Nzk2fQ.fTxdy_7X63-ypQnYib42HMYQ2_Zwa3o16BvBTwsugjI
'''

class Verify(ABC):

    class PasswordUpdate(BaseModel):
        pass

    class SecretJWTUpdate(BaseModel):
        pass

    class secret_jwt:
        def __init__(self, data) -> None:
            pass

    class password:
        def __init__(self) -> None:
            pass

        def change_password(self, data):
            pass


class UpdateUser(Verify):

    global PasswordUpdate
    global SecretJWTUpdate

    class PasswordUpdate(BaseModel):
        email: EmailStr
        password: str
        new_password: str
    
    class SecretJWTUpdate(BaseModel):
        email: EmailStr
        password: str

    class secret_jwt:

        #@nb.jit(nopython=True)
        def __init__(self, data: SecretJWTUpdate) -> None:
            
            '''
            Valida el empleado y si existe, y si existe crea una nueva clave jwt secreta para el
            usuario, lo guarda en el db y le da al usuario el "token_data" encriptado con su clave secreta

            Structure: {
                email: "example@gmail.com",
                password: "example"
            }

            Types of errors: 
            - UNKNOWN_ERROR
            - SubErrors:
                - ValidationUser()
                - JWToken.create()
            

            Response: {
                "info": "Clave cambiada correctamente y jwt creado correctamente",
                "status": "ok",
                "type": "SUCCESS",
                "data": {
                    "token": jwt
                } 
            }
            '''

            try:
                email: str = data["email"]
                password: str = data["password"]

                validation_user = ValidationUser({
                    "email": email,
                    "password": password,
                    "info": False
                })

                logger.info("validation_user: %s", validation_user)

                #Si el usuario esta de la forma correcta añadera el secreto de jwt en su profile
                if validation_user.response["status"] == "ok":
                    
                    #Genera el secreto
                    secret = str(secrets_generator(120))
                    encrypted_secret_key = encrypt(secret)

                    user_id = validation_user.response["data"]

                    workers.update_one(
                        { "_id": ObjectId(user_id) },
                        { "$set": {"data.secrets.jwt": encrypted_secret_key} }
                    )

                    jwt = JWToken.create({
                        "email": data["email"],
                        "password": data["password"]
                    }, secret)


                    if jwt["status"] == 'ok':
                        self.response = {
                            "info": "Clave cambiada correctamente y jwt creado correctamente",
                            "status": "ok",
                            "type": "SUCCESS",
                            "data": {
                                "token": jwt["token"]
                            } 
                        }
                    else:
                        self.response = jwt
                else:
                    self.response = validation_user.response


            except Exception as e:
                logger.info("Hubo un error inesperado: %s", e)
                self.response = {
                    "info": str(e),
                    "status": "no",
                    "type": "UNKNOWN_ERROR"
                }

    class password:

        def __init__(self, data: PasswordUpdate):
            try:
                self.response = None
                self.change_password(data)
            except Exception as e:
                self.response = {
                    "info": str(e),
                    "status": "no",
                    "type": "UNKNOWN_ERROR"
                }

        def change_password(self, data):

            validation_user = ValidationUser({
                "email": data["email"],
                "password": data["password"]
            })

            if validation_user.response["status"] == "ok":

                user_id = validation_user.response["data"]

                new_password: str = data["new_password"]
                encrypted_new_password: str = encrypt(new_password)

                # Actualizar la contraseña en la base de datos usando el ID del usuario
                workers.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"data.info.password": encrypted_new_password}}
                )
                self.response = {
                    "info": "Password updated successfully.",
                    "status": "ok",
                    "type": "PASSWORD_UPDATED"
                }
            else:
                self.response = {
                    "info": "Failed to update password.",
                    "status": "no",
                    "type": "PASSWORD_UPDATE_FAILED"
                }
