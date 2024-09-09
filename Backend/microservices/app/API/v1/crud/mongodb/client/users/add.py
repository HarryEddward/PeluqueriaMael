from pydantic import BaseModel, EmailStr
from pydantic import ValidationError, constr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from services.secrets_generator.main import secrets_generator
import numba as nb
from typing import Union
from Backend.microservices.app.API.v1.db.mongodb.database import users
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt
from Backend.microservices.app.API.v1.logging_config import logger

class InfoEncrypted(BaseModel):
    email: constr(max_length=100000)
    password: constr(max_length=100000)

class Info(BaseModel):
    email: EmailStr
    password: constr(max_length=75)

class Secrets(BaseModel):
    jwt: str

class Data(BaseModel):
    reservas: dict
    info: InfoEncrypted
    secrets: Secrets

class Add(BaseModel):
    data: Data

class AddUser:

    '''
    Se define el esquema Info, solo para añadir los datos necesarios
    al crear el usuario, y como ya esté creado, lo otro no lo hará
    uso hasta que haga otras acciones.

    El password tiene un máximo de 75 caracteres
    '''

    def __init__(self, info: Info):
        
        logger.info("Entra a AddUser")

        email: EmailStr = info["email"]
        password: str = info["password"]

        # Cifrar el email y el password
        encrypted_email = encrypt(email)
        encrypted_password = encrypt(password)
        
        logger.info(f"encrypted_email: {encrypted_email}")
        logger.info(f"encrypted_password: {encrypted_password}")

        # Crear el objeto Info, y verifica los atributos esten bien hechos. Como la verificación del email y el password
        Info(**{
            "email": email,
            "password": password
        })

        encrypted_info = InfoEncrypted(**{
            "email": encrypted_email,
            "password": encrypted_password
        })
        logger.info(f"encrypted_info: {encrypted_info}")

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

        logger.info("data to send: %s", self.data)

        self.response = None

        try:
            self.user_validated = self.verify(self.data)

            self.aggregate(self.user_validated)
            self.response = {"status": "ok"}

        except AttributeError as e:
            logger.error("Error a la hora de insertar el usuario INVALID_DATA: %s", e)
            self.response = {
                "info": f"El atributo no se encontró: {e}",
                "status": "no",
                "type": "INVALID_DATA"
            }
        except ValidationError as e:
            logger.error("Error a la hora de insertar el usuario VALIDATION_ERROR: %s", e)
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
            logger.info("USERVALDIATE: %s", user_validate)
            users.insert_one(user_validate)

        except Exception as e:
            logger.error("Error a la hora de insertar el usuario: %s", e)
            self.response = {
                "info": str(e),
                "status": "no",
                "type": "DATABASE_ERROR"
            }
