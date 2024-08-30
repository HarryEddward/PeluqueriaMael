from pydantic import BaseModel, EmailStr
#from pydantic import EmailStr

class schemes:
    #Login & Register
    class Credentials(BaseModel):
        email: EmailStr
        password: str

    #Login
    class Token(BaseModel):
        token: str

    #Register
    class NewUser(BaseModel):
        user: str
        psw: str
        email: str
    
    class TokenCredentials(BaseModel):
        token_id: str
        token_data: str