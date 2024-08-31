from pydantic import BaseModel, EmailStr
from pydantic import ValidationError
from pydantic_extra_types.phone_numbers import PhoneNumber
from services.secrets_generator.main import secrets_generator
import numba as nb
from Backend.microservices.app.API.v1.db.mongodb.database import users
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt

class Info(BaseModel):
    email: EmailStr
    password: str

class Secrets(BaseModel):
    jwt: str

class Data(BaseModel):
    reservas: dict
    info: Info
    secrets: Secrets

class Add(BaseModel):
    data: Data

class AddUser:

    '''
    Se define el esquema Info, solo para añadir los datos necesarios
    al crear el usuario, y como ya esté creado, lo otro no lo hará
    uso hasta que haga otras acciones.
    '''

    def __init__(self, info: Info):
        
        # Cifrar el email y el password
        encrypted_email = encrypt(info.email)
        encrypted_password = encrypt(info.password)
        
        # Crear el objeto Info cifrado
        encrypted_info = Info(
            email=encrypted_email,
            password=encrypted_password
        )
        
        # Crear el JWT cifrado
        jwt_token = encrypt(str(secrets_generator(120)))
        
        self.data = {
            "data": {
                "reservas": {},
                "info": encrypted_info,
                "secrets": {
                    "jwt": jwt_token
                }
            }
        }

        self.response = None

        try:
            self.user_validated = self.verify(self.data)

            self.aggregate(self.user_validated)
            self.response = {"status": "ok"}

        except AttributeError as e:
            self.response = {
                "info": f"El atributo no se encontró: {e}",
                "status": "no",
                "type": "INVALID_DATA"
            }
        except ValidationError as e:
            self.response = {
                "info": f"Al validar los datos hubo un error: {e}",
                "status": "no",
                "type": "VALIDATION_ERROR"
            }
        except Exception as e:
            self.response = {
                "info": str(e),
                "status": "no",
                "type": "UNKNOW_ERROR"
            }

    def verify(self, data: dict):
        user = Add(**data)
        return user.model_dump()

    def aggregate(self, user_validate):
        try:
            users.insert_one(user_validate)

        except Exception as e:
            self.response = {
                "info": str(e),
                "status": "no",
                "type": "DATABASE_ERROR"
            }
