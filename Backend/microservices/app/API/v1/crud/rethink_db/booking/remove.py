from pydantic import BaseModel, constr
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
    """
    Quita reservas no verificadas en RethinkDB

    Args:
        Verify ([type]): ABS Class
    """

    class Structure(BaseModel):
        date: datetime
        appointment_id: constr(max_length=50)
        personal_type: constr(max_length=200)
        personal_id: constr(max_length=200)

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
            cursor: net.DefaultCursor = reservas.filter({"fecha": formatted_date}).run(connection)
            sheet_list: list = list(cursor)

            if not sheet_list:
                return {
                    "info": "No se encontró la reserva para actualizar.",
                    "status": "no",
                    "type": "NOT_FOUND"
                }

            sheet_id: str = sheet_list[0]['id']
            document = sheet_list[0]  # Obtener el documento

            # Eliminar el appointment_id del documento en Python
            try:
                del document['professionals'][self.personal_type][self.personal_id][self.appointment_id]
            except KeyError:
                return {
                    "info": "No se encontró la cita en la estructura.",
                    "status": "no",
                    "type": "APPOINTMENT_NOT_FOUND"
                }

            # Actualizar el documento en la base de datos
            reservas.get(sheet_id).replace(document).run(connection)

            return {
                "info": "Se quitó la cita en la base de datos en tiempo real",
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
        "date": datetime(2024, 12, 9),
        "personal_id": "peluquero_2",
        "personal_type": "peluqueros",
        "appointment_id": "84dc0ae9-368d-4e82-9939-c1ddbb5a8c12"
    }

    booking_data: RemoveBooking.Structure = RemoveBooking.Structure(**data)
    booking: RemoveBooking = RemoveBooking(booking_data)

    print(booking.response)
