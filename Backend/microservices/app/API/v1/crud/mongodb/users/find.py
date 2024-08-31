from pydantic import BaseModel, EmailStr
from pydantic import ValidationError
from bson import ObjectId
from typing import Union
import numba as nb
from .validation import ValidationUser
from Backend.microservices.app.API.v1.db.mongodb.database import users
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt

class Find(BaseModel):
    email: EmailStr

global FindSecretJWTCredentials
class FindSecretJWTCredentials(BaseModel):
    email: EmailStr
    password: str
        
global FindSecretJWTID
class FindSecretJWTID(BaseModel):
    id: str


class FindUser:
    class info:

        #@nb.jit(nopython=True)
        def __init__(self, find: Find) -> None:
            self.email = encrypt(find.email)

            try:
                self.found = users.find_one({
                    "data.info.email": self.email
                })
                self.found = decrypt(self.found)

                if self.found:
                    self.response = {
                        "info": f"Se encontró un usuario con el email: {self.found}",
                        "status": "no",
                        "type": "FOUND_USER"
                    }
                else:
                    self.response = {
                        "info": f"No se encontró ningún usuario con el email: {self.found}",
                        "status": "no",
                        "type": "NO_FOUND_USER"
                    }
            except AttributeError as e:
                self.response = {
                    "info": str(e),
                    "status": "no",
                    "type": "ATTRIBUTE_ERROR"
                }
            except Exception as e:
                self.response = {
                    "info": str(e),
                    "status": "no",
                    "type": "UNKNOWN_ERROR"
                }

    class secret_jwt:
        
        #@nb.jit(nopython=True)
        def __init__(self, data: Union[FindSecretJWTCredentials, FindSecretJWTID]):
            self.response = None

            
            
            if isinstance(data, FindSecretJWTCredentials):

                data = data.model_dump()
                #print(data)
                try:
                    user_validate = ValidationUser({
                        "email": data.email,
                        "password": data.password
                    })

                    if user_validate.response["status"] == 'ok':
                        user_id = user_validate.response["data"]
                        user = users.find_one({ "_id":  ObjectId(user_id)})
                        jwt = user["data"]["info"]["secrets"]["jwt"]
                        if user:
                            if jwt:
                                self.response = {
                                    "info": "JWT secret obtenido exitosamente",
                                    "status": "ok",
                                    "type": "SUCCESS",
                                    "data": jwt
                                }
                            else:
                                self.response = {
                                    "info": "No se encontró el JWT secret para el usuario",
                                    "status": "error",
                                    "type": "JWT_SECRET_NOT_FOUND"
                                }
                        else: 
                            self.response = {
                                "info": "Usuario no encontrado",
                                "status": "no",
                                "type": "USER_NOT_FOUND"
                            }
                    else:
                        self.response = user_validate.response
                except Exception as e:
                    self.response = {
                        "info": str(e),
                        "status": "no",
                        "type": "UNKNOWN_ERROR"
                    }
            elif isinstance(data, FindSecretJWTID):
                
                data = data.model_dump()
                try:
                    print(data)
                    user = users.find_one({"_id": ObjectId(data["id"])})
                    print(user)

                    if user:
                        try:
                            secret = user["data"]["secrets"]["jwt"]
                            self.response = {
                                "info": "Se encontró la clave privada del usuario para el JWT",
                                "status": "ok",
                                "type": "SUCCESS",
                                "data": secret
                            }
                        except KeyError:
                            self.response = {
                                "info": "El atributo secret del usuario en la base de datos no se encuentra",
                                "status": "no",
                                "type": "NOT_FOUND_SECRET_JWT"
                            }
                    else:
                        self.response = {
                            "info": "El usuario no se encontró",
                            "status": "no",
                            "type": "USER_NOT_FOUND"
                        }
                except Exception as e:
                    self.response = {
                        "info": str(e),
                        "status": "no",
                        "type": "UNKNOWN_ERROR"
                    }
