from typing import Any
from pydantic import BaseModel
from abc import abstractmethod, ABC
from typing import Union
from Backend.microservices.app.API.v1.db.mongodb.database import reservas


class Verify(ABC):
    
    @abstractmethod
    def __call__(self) -> int:
        pass

    @abstractmethod
    def delete_appointments(self) -> None:
        pass



class RemoveAllAppointments(Verify):

    def __call__(self) -> int:
        return self.delete_appointments()

    def delete_appointments(self) -> Union[int, Exception]:

        """
        Elimina todas las fichas de reserva del db.
        """
        return reservas.delete_many({})


if __name__ == "__main__":

    remove_all: None = RemoveAllAppointments()
    remove_all()