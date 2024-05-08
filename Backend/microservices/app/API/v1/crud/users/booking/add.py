#-> ChatGPT debera de comprobar si el codigo sin protección esta bien para hacerse uso

from db.database import users
from pydantic import BaseModel, EmailStr
from pydantic import ValidationError
from bson import ObjectId
import datetime
from datetime import datetime
import numba as nb

class AddAppointment(BaseModel):
    day: int
    month: int
    year: int
    responsable_appointment: str
    id_appointment: str
    period: str
    start_time: str
    person_id: str
    service: str

class AddBookingUser:

    '''
    '''

    


    #@nb.jit(nopython=True)
    def __init__(self, data_raw: AddAppointment) -> None:
        self.response = {}

        data = data_raw.model_dump()

        responsable_appointment = data["responsable_appointment"]
        id_appointment = data["id_appointment"]
        period = data["period"]
        start_time = data["start_time"]
        person_id = data["person_id"]
        service = data["service"]
        day_date = data["day"]
        month_date = data["month"]
        year_date = data["year"]

        day = datetime(
            year_date,
            month_date,
            day_date
        )

        # Encuentra al usuario
        user = users.find_one({ "_id": ObjectId(person_id) })

        if user:
            # Define los datos de la reserva
            booking_data = {
                "service": service,
                "period": period,
                "start_time": start_time,
                "responsable_appointment": responsable_appointment,
                "date_appointment": day
            }

            # Actualiza el usuario con la nueva reserva
            update_result = users.update_one(
                { "_id": ObjectId(person_id) },
                { "$set": { f"reservas.{id_appointment}": booking_data } }
            )

            if update_result.modified_count > 0:
                self.response = {
                    "info": f"Reserva agregada al usuario {person_id}.",
                    "status": "ok",
                    "type": "SUCCESS"  # Tipo de éxito
                }
            else:
                self.response = {
                    "info": "Error al agregar reserva al usuario.",
                    "status": "no",
                    "type": "DATABASE_ERROR"  # Tipo de error de base de datos
                }
        else:
            self.response = {
                "info": "Usuario no encontrado en la base de datos.",
                "status": "no",
                "type": "DATABASE_ERROR"  # Tipo de error de base de datos
            }  


        


