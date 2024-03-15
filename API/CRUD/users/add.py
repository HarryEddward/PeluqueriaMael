from API.database import users
from pydantic import BaseModel

class Add(BaseModel):
    data: data

class data(BaseModel):
    reservas: dict
    info: dict


