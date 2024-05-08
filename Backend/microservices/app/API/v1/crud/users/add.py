from db.database import users
from pydantic import BaseModel, EmailStr
from pydantic import ValidationError
from pydantic_extra_types.phone_numbers import PhoneNumber
from services.secrets_generator.main import secrets_generator
import numba as nb

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
    Se define el esquema Info, solo para añadir los datos neecsarios
    al crear el usuario, y como ya este creado, lo otro no lo hara
    uso hasta que haga otras acciónes
    '''

    #@nb.jit(nopython=True)
    def __init__(self, info: Info):

        self.data = {
            "data": {
                "reservas": {},
                "info": info,
                "secrets": {
                    "jwt": str(secrets_generator(120))
                }
            }
        }

        self.response = None

        try:
            self.user_validated = self.verify(self.data)

            #print('user_Validate->', self.user_validated)
            self.aggregate(self.user_validated)
            self.response = {"status": "ok"}

        except AttributeError as e:
            self.response = {
                "info": f"El atributo no se encontro: {e}",
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

    #@nb.jit(nopython=True)
    def verify(self, data: dict):
        
        user = Add(**data)
        return user.model_dump()

    #@nb.jit(nopython=True)
    def aggregate(self, user_validate):
        try:
            users.insert_one(user_validate)

        except Exception as e:
            self.response = {
                "info": str(e),
                "status": "no",
                "type": "DATABASE_ERROR"
            }