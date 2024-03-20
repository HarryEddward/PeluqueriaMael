from API.database import users
from pydantic import BaseModel

class Add(BaseModel):
    data: data

class data(BaseModel):
    reservas: dict
    info: dict

class info(BaseModel):
    pass

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


def add_user(data: dict):
    pass
