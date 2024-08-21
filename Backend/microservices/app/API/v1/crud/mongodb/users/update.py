from Backend.microservices.app.API.v1.db.mongodb.database import users
from pydantic import BaseModel, EmailStr
from pydantic import ValidationError
from services.secrets_generator.main import secrets_generator
from bson import ObjectId
import numba as nb

from .validation import ValidationUser
from services.auth import JWToken



'''
Aquí estaran todos los métodos que se haran uso, estan de forma controlada
para que no se puedan modificar cualquier dato que nos de la gana.
Para evitar fallos de seguirdad

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjp7ImVtYWlsIjoiYWRyaWFuZWxjYXBvQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiZnVja195b3UifSwiZXhwIjoxNzE1NjI3Nzk2fQ.fTxdy_7X63-ypQnYib42HMYQ2_Zwa3o16BvBTwsugjI
'''

class UpdateUser:

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
        def __init__(self, data: SecretJWTUpdate):
            
            '''
            Valida el usurio y si existe, y si existe crea una nueva clave jwt secreta para el
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
                print('1-> update jwt', data)

                validation_user = ValidationUser({
                    "email": data["email"],
                    "password": data["password"],
                    "info": False
                })
                print('2-> update jwt', validation_user)

                #Si el usuario esta de la forma correcta añadera el secreto de jwt en su profile
                if validation_user.response["status"] == "ok":
                    
                    #Genera el secreto
                    secret = str(secrets_generator(120))
                    print('3-> update jwt', secret)
                    print('secret ->', secret) 
                    print('_id ->', validation_user.response["data"]) #<- Posible Error

                    user_id = validation_user.response["data"]
                    print('4-> update jwt', user_id)

                    users.update_one(
                        { "_id": ObjectId(user_id) },
                        { "$set": {"data.secrets.jwt": secret} }
                    )

                    jwt = JWToken.create({
                        "email": data["email"],
                        "password": data["password"]
                    }, secret)

                    print('5-> update jwt', jwt)

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
                self.response = {
                    "info": str(e),
                    "status": "no",
                    "type": "UNKNOWN_ERROR"
                }

    class password:

        #@nb.jit(nopython=True)
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

        #@nb.jit(nopython=True)
        def change_password(self, data):

            validation_user = ValidationUser({
                "email": data["email"],
                "password": data["password"]
            })

            print('1->', validation_user.response)

            if validation_user.response["status"] == "ok":

                user_id = validation_user.response["data"]

                print('2->', user_id)
                print('pasw ->', data["new_password"])
                # Actualizar la contraseña en la base de datos usando el ID del usuario
                users.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"data.info.password": data["new_password"]}}
                )
                self.response = {
                    "info": "Password updated successfully.",
                    "status": "ok",
                    "type": "PASSWORD_UPDATED"
                }
            else:
                print('3-> Faildes update password')
                self.response = {
                    "info": "Failed to update password.",
                    "status": "no",
                    "type": "PASSWORD_UPDATE_FAILED"
                }
