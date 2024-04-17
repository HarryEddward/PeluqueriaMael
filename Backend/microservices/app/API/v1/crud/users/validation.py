from db.database import users
from pydantic import BaseModel, EmailStr


class Credentials(BaseModel):
    email: EmailStr
    password: str
    info: bool = False


class ValidationUser:

    def __init__(self, data: Credentials):
        '''
        Validar si el usuario exite, si existe, devolver el id del db

        Structure: {
            email: "example@gmail.com",
            password: "example",
            info: (Default: False)
        }

        What is info?:
        - Info refers if you want more data and return the all information of the user, but if you dont want the all data, you can give the id user in the db 

        Types of errors: 
        - UNKNOWN_ERROR
        - USER_NOT_FOUND
        - INCORRECT_PASSWORD
        - DATABASE_ERROR

        Response: {
            "info": "Password validation successful.",
            "status": "ok",
            "type": "PASSWORD_VALIDATED",
            "data": "id_database" / user_document
        }

        How to access:
        - user = Validation()
        - [ user.response ] 
        '''
        try:
            self.response = None
            self.search_user(data)
        except Exception as e:
            self.response = {
                "info": str(e),
                "status": "no",
                "type": "UNKNOWN_ERROR"
            }

    def search_user(self, data):
        user = users.find_one({"data.info.email": data["email"]})
        print('user -> ', user)
        if user:
            self.validate_password(user, data)
        else:
            self.response = {
                "info": "User not found.",
                "status": "no",
                "type": "USER_NOT_FOUND"
            }

    def validate_password(self, user, data):


        try:
            if user["data"]["info"]["password"] == data["password"]:
                
                if data["info"] != False:
                    self.data = dict(user)
                else:
                    self.data = str(user["_id"])

                self.response = {
                    "info": "Password validation successful.",
                    "status": "ok",
                    "type": "PASSWORD_VALIDATED",
                    "data": self.data
                }
            else:
                self.response = {
                    "info": "Incorrect password.",
                    "status": "no",
                    "type": "INCORRECT_PASSWORD"
                }
        except Exception as e:
                    # Capturar y manejar el error de la base de datos
            self.response = {
                "info": "Database error: " + str(e),
                "status": "no",
                "type": "DATABASE_ERROR"
            }
