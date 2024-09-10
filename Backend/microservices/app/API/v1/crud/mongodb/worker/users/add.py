from abc import ABC
from typing import Any, Union
from datetime import datetime
from pydantic import BaseModel, constr, EmailStr, field_validator, ValidationError
from Backend.microservices.app.API.v1.services.secrets_generator.main import secrets_generator
from Backend.microservices.app.API.v1.db.mongodb.database import workers
from Backend.microservices.conversor.config.config import Config
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt

config: dict = Config()
config_api: dict = config["app"]["API"]["validation"]["user"]
max_str_email: int = config_api["email"]["max_str"]
min_str_email: int = config_api["email"]["min_str"]
max_str_password: int = config_api["password"]["max_str"]
min_str_password: int = config_api["password"]["min_str"]


class Verify(ABC):
    def __call__(self) -> Union[dict, Exception, ValidationError]:
        pass

    def register_worker(self) -> None:
        pass

class RequestStructureInfo(BaseModel):
    email: constr(max_length=max_str_email, min_length=min_str_email)
    password: constr(max_length=max_str_password, min_length=min_str_password)

class RequestStructureSecrets(BaseModel):
    jwt: constr(max_length=50000)

class RequestStructureData(BaseModel):
    info: RequestStructureInfo
    secrets: RequestStructureSecrets

class ValidateRequestMongoDB(BaseModel):
    day_of_creation: datetime
    data: RequestStructureData

class StrutureAddUserWorker(BaseModel):
    email: EmailStr
    password: constr(max_length=max_str_password, min_length=min_str_password)

    @field_validator("email")
    @classmethod
    def check_min_and_max_length_email(cls, value):
        if not (min_str_email <= len(value.strip()) <= max_str_email):
            raise ValidationError("ERROR_EMAIL_LENGTH")
        return value

    @field_validator("password")
    @classmethod
    def check_min_and_max_length_password(cls, value):
        if not (min_str_password <= len(value.strip()) <= max_str_password):
            raise ValidationError("ERROR_PASSWORD_LENGTH")
        return value

class AddUserWorker(Verify):
    def __call__(self, data_raw: StrutureAddUserWorker) -> Union[dict, Exception, ValidationError]:
        try:
            data: dict = data_raw.model_dump()
            self.email: str = data["email"]
            self.password: str = data["password"]
            self.email_encrypted: str = encrypt(self.email)
            self.password_encrypted: str = encrypt(self.password)

            self.secret_jwt_token: str = encrypt(str(secrets_generator(120)))
            self.day_of_creation: datetime = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            try:
                validated_data = self.verify_structure_request({
                    "day_of_creation": self.day_of_creation,
                    "data": {
                        "info": {
                            "email": self.email_encrypted,
                            "password": self.password_encrypted
                        },
                        "secrets": {
                            "jwt": self.secret_jwt_token
                        }
                    }
                })
            except Exception as e:
                return {
                    "info": f"Hubo un fallo a la hora de revisar la estructura a la estrctura del usuario a crear: {e}",
                    "status": "no",
                    "type": "ERROR_VALIDATE_STRUCTURE_PYDANTIC"
                }
            
            try:
                return self.register_worker(validated_data)
            except Exception as e:
                return {
                    "info": f"Hubo un error a la hora de añadir el usuario del trabajador en la base de datos en MongoDB: {e}",
                    "status": "no",
                    "type": "ERROR_DATABASE_MONGODB_ADD_WORKER"
                }

        except Exception as e:
            return {
                "info": f"Hubo un error global en add user worker: {e}",
                "status": "no",
                "type": "ERROR_ADD_USER_WORKER"
            }

    def verify_structure_request(self, validate_data: ValidateRequestMongoDB) -> Union[ValidateRequestMongoDB, Exception]:
        return validate_data

    def register_worker(self, safe_data: dict) -> Union[None, Exception]:
        workers.insert_one(safe_data)


if __name__ == "__main__":
    print(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
    # Crear la clase 'struture' con la longitud máxima de email
    struture_add_user_worker = StrutureAddUserWorker(
        email="user@gmail.com",
        password="Password"
    )
    instance_add_user_worker = AddUserWorker()
    result_add_user_worker = instance_add_user_worker(struture_add_user_worker)
    print(result_add_user_worker)
