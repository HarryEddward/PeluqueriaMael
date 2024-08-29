from pydantic import BaseModel, constr
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4
from Backend.microservices.app.API.v1.logging_config import logger
from Backend.microservices.app.API.v1.db.rethink_db.database import reservas, connection


class Verify(ABC):

    class structure(BaseModel):
        pass

    @abstractmethod
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def add_booking(self) -> dict:
        pass

class AddBooking(Verify):
    """
    Crea reservas no verificadas en RethinkDB.
    """

    class structure(BaseModel):
        user: constr(max_length=32)
        date: datetime
        hour: constr(max_length=10)
        id_appointment: constr(max_length=50)
        personal_type: constr(max_length=50)
        personal_id: constr(max_length=50)

    def __init__(self, data_raw: structure) -> None:
        data: dict = data_raw.model_dump()  # Cambiado de model_dump() a dict()
        
        logger.info(f"Data -> {data}")

        self.date: datetime = data["date"]
        self.personal_type: str = data["personal_type"]
        self.personal_id: str = data["personal_id"]
        self.user: str = data["user"]
        self.hour: str = data["hour"]
        self.id_appointment: str = data["id_appointment"]

        try:
            self.response = self.add_booking()
        except Exception as e:
            self.response = {
                "info": f"Error desconocido del servidor: {e}",
                "status": "no",
                "type": "UNKNOWN_ERROR"
            }

    def add_booking(self) -> dict:
        try:
            request: dict = {
                "user": self.user,
                "hour": self.hour
            }

            # Formatear la fecha como ISO 8601 para la base de datos
            formatted_date: datetime.isoformat = self.date.isoformat()
            
            logger.info(f"Fecha: {formatted_date}")
            # Buscar el documento por un identificador único (ej. fecha)
            cursor = reservas.filter({"fecha": formatted_date}).run(connection)
            sheet_list = list(cursor)  # Convertir el cursor a una lista

            if not sheet_list:
                return {
                    "info": "No se encontró la reserva para actualizar.",
                    "status": "no",
                    "type": "NOT_FOUND"
                }

            sheet_id = sheet_list[0]['id']  # Asumiendo que el id es un campo en el documento

            # Actualizar el documento usando la clave dinámica
            reservas.get(sheet_id).update({
                "professionals": { 
                    str(self.personal_type): {
                        str(self.personal_id): {
                            str(self.id_appointment): request
                        }
                    }
                }
            }).run(connection)

            return {
                "info": "Cita añadida en la base de datos en tiempo real",
                "status": "ok",
                "type": "SUCCESS"
            }

        except Exception as e:
            return {
                "info": f"Error desconocido del servidor: {e}",
                "status": "no",
                "type": "RETHINK_DB_DATABASE_ERROR"
            }

if __name__ == "__main__":
    data: dict = {
        "user": "john_doe",
        "date": datetime(2024, 12, 9),
        "hour": "10:00 AM",
        "id_appointment": str(uuid4()),
        "personal_type": "peluqueros",
        "personal_id": "peluquero_2"
    }

    booking_data: AddBooking.structure = AddBooking.structure(**data)
    booking: AddBooking = AddBooking(booking_data)

    print(booking.response)
