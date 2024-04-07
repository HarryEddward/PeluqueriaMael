from db.database import users
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
        return {
            "info": "",
            "status": "ok",
            "type": "SUCCESS"
        }
    
    except AttributeError:
        return {
            "info": "INVALID_DATA",
            "status": "no",
            "type": ""
        }
    except ValidationError:
        return {
            "info": "",
            "status": "no",
            "type": ""
        }
    except Exception as e:
        return {
            "info": "",
            "status": "no",
            "type": ""
        }


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
    

