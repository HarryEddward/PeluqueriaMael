from API.database import users
from pydantic import BaseModel
from pydantic import ValidationError
from pydantic_extra_types.phone_numbers import PhoneNumber


class Info(BaseModel):
    username: str
    number_phone: PhoneNumber
    password: str

class Data(BaseModel):
    reservas: dict
    info: Info

class Add(BaseModel):
    data: Data


'''
STRUCTURE:

{
    id,
    data: {
        reservas: {},
        info: {
            username: str,
            number_phone: str,
            password: str
        }
    }
    
}
'''


def add_user(data: Add):

    try:
        print(data)
        user_validate = Add(**data)
        print(user_validate)
        return 0
    
    except AttributeError:
        print('La validación falló')
    except ValidationError:
        print('La validación falló')
    except Exception as e:
        print(e)
        print('heloooooooo')


input_data = {
    "data": {
        "reservas": {},
        "info": {
            "username": 10,
            "number_phone": "+3443567016",
            "password": "contrasena123"
        }
    }
}
hola = add_user(input_data)
    

