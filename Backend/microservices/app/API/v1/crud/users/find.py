from ...db.database import users
from pydantic import BaseModel, EmailStr
from pydantic import ValidationError


class Find(BaseModel):
    email: EmailStr


'''
Encuentra el usuario a aprtir de su email, porque el email?
Al un futuro verificar el email, seria como también un nombre usuario y se podria
validar su correo
'''
class FindUser:

    def __init__(self, find: Find) -> None:

        self.email = find["email"]

        try:
            self.found = users.find_one({"data.info.email": self.email})
            print(self.found)

            if self.found:
                self.response = {
                    "info": f"Se encontró un usuario con el email: {self.email}",
                    "status": "ok",
                    "type": "FOUND_USER"
                }
            elif self.found == None:
                self.response = {
                    "info": f"No se encontro ningún usuario con el email: {self.email}",
                    "status": "ok",
                    "type": "NO_FOUND_USER"
                }

        except AttributeError as e:

            self.response = {
                "info": str(e),
                "status": "no",
                "type": "ATTRIBUTE_ERROR"
            }

        except Exception as e:

            self.response = {
                "info": str(e),
                "status": "no",
                "type": "UNKNOW_ERROR"
            }