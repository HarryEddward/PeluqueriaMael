from db.database import users
from pydantic import BaseModel, EmailStr
from bson import ObjectId

class RemoveBookingUser:
    class structure(BaseModel):
        id_appointment: str
        person_id: str

    def __init__(self, data_raw: structure) -> None:
        self.response = None

        data = data_raw.model_dump()
        id_appointment = data["id_appointment"]
        person_id = data["person_id"]

        try:
            user = users.find_one({ "_id": ObjectId(person_id) })
            if not user:
                self.response = {
                    "info": f"No se encontró el usuario con ID {person_id}.",
                    "status": "no",
                    "type": "USER_NOT_FOUND"
                }
                return

            reservation = user.get("reservas", {}).get(id_appointment)
            if not reservation:
                self.response = {
                    "info": f"No se encontró la reserva con ID {id_appointment} en el usuario con ID {person_id}.",
                    "status": "no",
                    "type": "NOT_FOUND_APPOINTMENT"
                }
                return

            update_result = users.update_one(
                { "_id": ObjectId(person_id) },
                { "$unset": { f"reservas.{id_appointment}": "" } }
            )

            if update_result.modified_count > 0:
                self.response = {
                    "info": f"Se eliminó correctamente la reserva con ID {id_appointment} del usuario con ID {person_id}.",
                    "status": "ok",
                    "type": "SUCCESS"
                }
            else:
                self.response = {
                    "info": f"No se pudo eliminar la reserva con ID {id_appointment} del usuario con ID {person_id}.",
                    "status": "no",
                    "type": "ERROR_REMOVE_APPOINTMENT"
                }

        except Exception as e:
            self.response = {
                "info": f"Error en la base de datos: {e}",
                "status": "no",
                "type": "DATABASE_ERROR"
            }
