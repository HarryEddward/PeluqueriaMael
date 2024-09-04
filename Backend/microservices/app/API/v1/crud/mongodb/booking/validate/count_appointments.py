from typing import Any
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Union
from bson import ObjectId
from Backend.microservices.conversor.config.config import Config
from Backend.microservices.app.API.v1.db.mongodb.database import users
from Backend.microservices.app.API.v1.logging_config import logger


class Verify(ABC):
    
    def __call__(self) -> Union[dict, Exception]:
        pass
    
    def obtain_appointments(self) -> Union[list, Exception]:
        pass

    def evaluate_results(self) -> Union[dict, Exception]:
        pass

class CountAppointmentsModel(BaseModel):
    user_id: str

class CountAppointments(Verify):


    def __init__(self) -> None:
        self.max_appointments: dict = Config()
        self.max_appointments: str = self.max_appointments["app"]["API"]["validation"]["user"]["max_appointments"]

    def __call__(self, data_raw: CountAppointmentsModel) -> Union[dict, Exception]:
        
        try:
            data: dict = data_raw.model_dump()
            self.user_id: str = data["user_id"]
        except Exception as e:
            return {
                "info": "Error a la extracción de los datos validados",
                "status": "no",
                "type": "PYDANTIC_ERROR_EXTRACTION"
            }
        
        try:
            self.list_appointments: list = self.obtain_appointments()
        except Exception as e:
            return {
                "info": "Error a la hora de buscar en la base de datos el usuario",
                "status": "no",
                "type": "DATABASE_ERROR"
            }
        
        try:
            result = self.evaluate_results(self.list_appointments)

            if not result:
                return {
                    "info": f"Solo se permiten máximo {self.max_appointments} reservas en tu perfil",
                    "status": "no",
                    "type": "EXCEDED_DAYS"
                }
            
            return {
                "info": "Puedes hacer tu reserva de forma exitosa",
                "status": "ok",
                "type": "SUCCESS"
            }

        except Exception as e:
            return {
                "info": "Error a la hora de evaular las reservas",
                "status": "no",
                "type": "EVALUATE_ERROR"
            }
    
    def obtain_appointments(self) -> Union[list, Exception]:
        """
        Devulve una lista sobre las reservas que tiene, si no tiene
        devuelve una lista vacia, y si las hay obtiene el id's de las
        reservas.

        Returns:
            Union[list, Exception]: [description]
        """

        document: dict = users.find_one({"_id": ObjectId(self.user_id)})
        #logger.info(f"DOC: {document}")

        count: Union[None, dict] = document["data"]["reservas"]
        
        if not count:
            return []
        
        return count.keys()


    def evaluate_results(self, data: list) -> Union[dict, Exception]:

        """
        Evalua si supera el maximo permitido de reservas, si supera
        el máximo permitido dara un resultado negativo [False] y de
        froma dinamica se puede controlar a partir de un archivo yml
        el máximo permitido de reservas.

        Returns:
            [bool]: [Devuelve un resultado negativo o positivo]
        """
        
        return len(data) < self.max_appointments



if __name__ == "__main__":
    data_count_appointments = CountAppointmentsModel(user_id="66d624307bdc4aff296819f9")
    count_appointments = CountAppointments()
    result = count_appointments(data_count_appointments)
    print(result)