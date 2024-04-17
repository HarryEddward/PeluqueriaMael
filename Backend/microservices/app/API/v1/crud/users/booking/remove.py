#-> ChatGPT debera de comprobar si el codigo sin protección esta bien para hacerse uso

from db.database import users
from pydantic import BaseModel, EmailStr
from pydantic import ValidationError
from bson import ObjectId

from enum import Enum


class RemoveAppointment(BaseModel):
    id_appointment: str
    person_id: str

class RemoveBookingUser:

    '''
    Cuando se hace uso el RemoveBookingUser, se debe antes comprobar que el person_id exitse,
    porque no comprobará si existe o no. Directamente quitara la reserva, si que el error de un usuario
    no validado se debera de comprobar antes.

    No tiene proteccion de saber si existe o no el usuario id.

    Hize un simple cambio si el usuario existe, por su user_id, 
    '''

    def __init__(self, data: RemoveAppointment) -> None:
        self.response = None

        id_appointment = data["id_appointment"]
        person_id = data["person_id"]

        try:
            exist_id = users.find_one({ "_id": ObjectId(person_id) })

            # Actualiza el documento para eliminar la propiedad 'reservas' con el ID específico
            update_result = users.update_one(
                { "_id": ObjectId(person_id) },
                { "$unset": { f"reservas.{id_appointment}": "" } }
            )
        except Exception as e:
            self.response = {
                "info": f"Error en la base de datos: {e}",
                "status": "no",
                "type": "DATABASE_ERROR"
            }

        if not exist_id:
            self.response = {
                "info": f"No se encontro el usuario {person_id}.",
                "status": "no",
                "type": "USER_NOT_FOUND"
            }

        if not update_result:
            self.response = {
                "info": f"No se encontró la reserva con ID {id_appointment} en el usuario con ID {person_id}.",
                "status": "no",
                "type": "MISMATCH"
            }

        # Verifica si la operación se realizó correctamente
        if not update_result.modified_count > 0:
            self.response = {
                "info": f"No se encontró la reserva con ID {id_appointment} en el usuario con ID {person_id}.",
                "status": "no",
                "type": "MISMATCH"  # Tipo de error único
            }  
        
        self.response = {
                "info": f"Se eliminó correctamente la reserva con ID {id_appointment} del usuario con ID {person_id}.",
                "status": "ok"
            }
              


        


