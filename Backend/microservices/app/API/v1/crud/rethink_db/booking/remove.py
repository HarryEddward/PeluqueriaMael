from pydantic import (
    BaseModel,
    ValidationError,
    constr
)
from abc import ABC, abstractmethod
from datetime import datetime
from rethinkdb import r, net
from Backend.microservices.app.API.v1.db.rethink_db.database import reservas, connection

class Verify(ABC):

    class Structure(BaseModel):
        pass

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def remove_booking(self) -> dict:
        pass
    


class RemoveBooking(Verify):
    """AI is creating summary for AddBooking

    Args:
        Verify ([type]): ABS Class
    """
    
    class Structure(BaseModel):
        date: datetime
        id_appointment: constr(max_length=50)
        personal: constr(max_length=50)
        appointment_id: constr(max_length=50)

    def __init__(self, data_raw: Structure) -> None:
        self.response = {}

        data: dict = data_raw.model_dump()
        self.date: datetime = data["date"]
        self.personal_type: str = data["personal_type"]
        self.personal_id: str = data["personal_id"]
        self.appointment_id: str = data["appointment_id"]

        try:
            self.response = self.remove_booking()
        except Exception as e:
            self.response = {
                "info": f"Error desconocido del servidor: {e}",
                "status": "no",
                "type": "UNKNOWN_ERROR"
            }

    def remove_booking(self) -> dict:
        
        try:

            # Formatear la fecha como ISO 8601 para la base de datos
            formatted_date: datetime.isoformat = self.date.isoformat()

            # Obtener el documento actual
            cursor: net.DefaultCursor = reservas.filter({ "fecha": formatted_date }).run(connection)
            sheet_list: list = list(cursor)

            if not sheet_list:
                return {
                    "info": "No se encontró la reserva para actualizar.",
                    "status": "no",
                    "type": "NOT_FOUND"
                }
            
            sheet_id: str = sheet_list[0]['id']

            reservas.get(sheet_id).update({
                'profesionals': {
                    str(self.personal_type) : {
                        str(self.personal_id): r.row[str(self.personal_type)][str(self.personal_id)].without(self.appointment_id)
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
        "date": datetime(2024, 8, 10),
        "id_appointment": "",
        "personal": "",
        "appointment_id": ""
    }

    booking_data: RemoveBooking.Structure = RemoveBooking.Structure(**data)
    booking: RemoveBooking = RemoveBooking(booking_data)

    print(booking.response)