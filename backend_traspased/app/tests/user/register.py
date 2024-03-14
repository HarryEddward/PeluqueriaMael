import requests
from pydantic import BaseModel, EmailStr

url = "http://localhost:9712/user/register"


class Credentials(BaseModel):
    user: str
    psw: str
    email: EmailStr

class Token(BaseModel):
    token: str



#Usuario actual
token_data: Token = {
    "token": "eyJhbGciOiJIUzI1NiIssadadInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDAxNzcyOTEsInVzZXIiOiJKdWFuIiwicHN3IjoiMDlldTB3ZG9kMGF1ZCJ9.Ko82-uhkIrixYJbRzBuljqzRVQU85Yd-zsHNjFDuEvI"
}

#Nuevo usuario creado
credentials_data: Credentials = {
    "user": "Manuel",
    "psw": "12324324234",
    "email": "aunel@gmail.com"
}

response = requests.post(url, json=token_data)

print(response.json())
