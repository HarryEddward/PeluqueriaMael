from ...db.database import users
from pydantic import BaseModel, EmailStr


class Credentials(BaseModel):
    email: EmailStr
    password: str


class ValidationUser:

    def __init__(self, data: Credentials):
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
                self.response = {
                    "info": "Password validation successful.",
                    "status": "ok",
                    "type": "PASSWORD_VALIDATED",
                    "data": str(user["_id"])
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
