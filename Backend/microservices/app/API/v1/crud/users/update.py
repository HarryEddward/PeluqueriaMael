from ...db.database import users
from pydantic import BaseModel, EmailStr
from pydantic import ValidationError
from ...services.secrets_generator.main import secrets_generator
from bson import ObjectId

from .validation import ValidationUser
from ...services.auth import JWToken



'''
Aquí estaran todos los métodos que se haran uso, estan de forma controlada
para que no se puedan modificar cualquier dato que nos de la gana.
Para evitar fallos de seguirdad
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
        def __init__(self, data: SecretJWTUpdate):
            try:
                validation_user = ValidationUser({
                    "email": data["email"],
                    "password": data["password"]
                })

                #Si el usuario esta de la forma correcta añadera el secreto de jwt en su profile
                if validation_user.response["status"] == "ok":
                    
                    #Genera el secreto
                    secret = str(secrets_generator(120))
                    print('secret ->', secret) 
                    print('_id ->', validation_user.response["data"]) #<- Posible Error

                    user_id = validation_user.response["data"]

                    users.update_one(
                        { "_id": ObjectId(user_id) },
                        { "$set": {"data.secrets.jwt": str(secret)} }
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
