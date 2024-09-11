from abc import ABC
from typing import Any, Union
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, constr, EmailStr, field_validator, ValidationError
from Backend.microservices.app.API.v1.services.secrets_generator.main import secrets_generator
from Backend.microservices.app.API.v1.db.mongodb.database import workers
from Backend.microservices.conversor.config.config import Config
from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt

config: dict = Config()
config_api: dict = config["app"]["API"]["validation"]["user"]
max_str_user_id: int = config_api["user_id"]["max_str"]
min_str_user_id: int = config_api["user_id"]["min_str"]


class Verify(ABC):
    def __call__(self) -> Union[dict, Exception, ValidationError]:
        pass

    def register_worker(self) -> None:
        pass

class StrutureRemoveUserWorker(BaseModel):
    user_id: constr(max_length=max_str_user_id, min_length=min_str_user_id)

class RemoveUserWorker(Verify):
    def __call__(self, data_raw: StrutureRemoveUserWorker) -> Union[dict, Exception, ValidationError]:
        try:
            data: dict = data_raw.model_dump()
            self.user_id: str = data["user_id"]
            
            try:
                return self.delete_worker()
            except Exception as e:
                return {
                    "info": f"Hubo un error a la hora de añadir el usuario del trabajador en la base de datos en MongoDB: {e}",
                    "status": "no",
                    "type": "ERROR_DATABASE_MONGODB_REMOVE_WORKER"
                }

        except Exception as e:
            return {
                "info": f"Hubo un error global en add user worker: {e}",
                "status": "no",
                "type": "ERROR_REMOVE_USER_WORKER"
            }

    def delete_worker(self) -> Union[None, Exception]:
        workers.delete_one({ "_id": ObjectId(self.user_id) })


if __name__ == "__main__":
    # Crear la clase 'struture' con la longitud máxima de email
    struture_remove_user_worker = StrutureRemoveUserWorker(
        user_id="66e06a800de1a379504c3d97"
    )
    instance_remove_user_worker = RemoveUserWorker()
    result_remove_user_worker = instance_remove_user_worker(struture_remove_user_worker)
    print(result_remove_user_worker)
