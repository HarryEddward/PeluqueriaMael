from pydantic import (
    BaseModel,
    EmailStr
)

#Login & Register
class Credentials(BaseModel):
    number_phone: str
    password: str

#Login
class Token(BaseModel):
    token: str

#Register
class NewUser(BaseModel):
    user: str
    psw: str
    email: EmailStr