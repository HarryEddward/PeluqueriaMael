from db.database import reservas
from db.database import configure
import datetime
from config import config
import uuid
from crud.users.booking.add import AddBookingUser, AddAppointment
from bson import ObjectId
from utils.main import conversorServices
from pydantic import BaseModel



class AddBooking:

    class structure(BaseModel):
        day: str
        professional: str
        period: str
        start_time: str
        service_duration: str
        person_id: str
        service: str

    #request_appointment
    def __init__(
            self,
            data: Scheme
        ):
        '''
        Example = {
            Scheme(
                day: str
                professional: str
                period: str
                start_time: str
                service_duration: str
                person_id: str
                service: str
            )
        }

        Response = {
        
        }
        
        '''

        self.response = {}


        day: str = data["day"]
        professional: str = data["professional"]
        period: str = data["period"]
        start_time: str = data["start_time"]
        service_duration: str = data["service_duration"]
        person_id: str = data["person_id"]
        service: str = data["service"]
        
        #Obtiene la información de la reserva desde la base de datos del día especficado
        try:
            day_appointment = reservas.find_one({"fecha": {"$eq": day}})
            services_raw = configure.find_one({ "_id": ObjectId("65ec5f9f88701955b30661a5") })
        except Exception as e:
            self.response = {
                "info": f"Error al programar la cita en la base de datos: {e}",
                "status": "no",
                "type": "DATABASE_ERROR"  # Tipo de error único
            }

        services = conversorServices(services_raw)
        professionals = day_appointment.get('professionals')

        morning_opening_time = config["morning_opening_time"]
        morning_closing_time = config["morning_closing_time"]
        afternoon_opening_time = config["afternoon_opening_time"]
        afternoon_closing_time = config["afternoon_closing_time"]

        start_time_dt = datetime.strptime(start_time, '%H:%M')  # Convertir start_time a datetime

        if period == 'morning':
            if start_time_dt < morning_opening_time or start_time_dt >= morning_closing_time:
                self.response = {
                    "info": "No se puede programar una cita en la mañana fuera del horario de apertura y cierre.",
                    "status": "no"
                }
        elif period == 'afternoon':
            if start_time_dt < afternoon_opening_time or start_time_dt >= afternoon_closing_time:
                self.response = {
                    "info": "No se puede programar una cita en la tarde fuera del horario de apertura y cierre.",
                    "status": "no"
                }

        id_appointment = str(uuid.uuid4())
        
        if period not in professionals[professional]:
            self.response = {
                "info": "El período especificado no es válido para este profesional.",
                "status": "no",
                "type": "ERROR1"  # Tipo de error único
            }

        morning_schedule = professionals[professional]['morning']
        last_hour_morning = str(max(morning_schedule.keys(), key=lambda x: datetime.strptime(x, "%H:%M")))
        
        if period == 'morning' and start_time >= last_hour_morning:
            self.response = {
                "info": "No se puede programar una cita en la mañana después del mediodía.",
                "status": "no",
                "type": "ERROR2"  # Tipo de error único
            }
        elif period == 'afternoon' and start_time < last_hour_morning:
            self.response = {
                "info": "No se puede programar una cita en la tarde antes del mediodía.",
                "status": "no",
                "type": "ERROR3"  # Tipo de error único
            }

        if start_time in professionals[professional][period]:
            end_time = (datetime.strptime(start_time, '%H:%M') + service_duration).strftime('%H:%M')

            # Verificar si la cita programada se extiende más allá del horario de cierre de la mañana o tarde
            if period == 'morning' and datetime.strptime(end_time, '%H:%M') > morning_closing_time:
                self.response = {
                    "info": f"No se puede programar la cita para {professional} después del horario de cierre de la mañana.",
                    "status": "no",
                    "type": "OUT_SCHULDE_BEFORE_MORNING"  # Tipo de error único
                }
            elif period == 'afternoon' and datetime.strptime(end_time, '%H:%M') > afternoon_closing_time:
                self.response = {
                    "info": f"No se puede programar la cita para {professional} después del horario de cierre de la tarde.",
                    "status": "no",
                    "type": "OUT_SCHULDE_AFTER_AFTERNOON"  # Tipo de error único
                }

            available_slots = list(professionals[professional][period].items())
            
            # Verificar si algún intervalo parcial está disponible
            start_datetime = datetime.strptime(start_time, '%H:%M')
            end_datetime = datetime.strptime(end_time, '%H:%M')
            
            overlapping_slots = [
                                    (slot, status) for slot, status in available_slots
                                    
                                    if start_datetime < datetime.strptime(slot, '%H:%M') < end_datetime
                                        or start_datetime <= datetime.strptime(slot, '%H:%M') < end_datetime
                                ]
            
            
            # Verificar si hay algún solapamiento en la franja horaria
            if overlapping_slots and any(status["status"] == 'ocupado' for _, status in overlapping_slots):
                self.response = {
                    "info": f"No se puede programar la cita para {professional} en la franja horaria solicitada.",
                    "status": "no",
                    "type": "PROFESSIONAL_BUSY"  # Tipo de error único
                }

            # Marcar el intervalo parcial como ocupado y guardar la información de la cita
            for slot, _ in available_slots:
                if start_datetime <= datetime.strptime(slot, '%H:%M') < end_datetime:
                    professionals[professional][period][slot] = {
                        "status": 'ocupado',
                        "info": {
                            "person_id": person_id,
                            "service": service,
                            "id_appointment": id_appointment,
                            
                        }
                    }
                    if slot != start_time:  # Solo limpiar 'info' en las franjas horarias distintas a la seleccionada
                        professionals[professional][period][slot].pop("info", None)

            

            addUserAppointment = AddBookingUser
            (
                AddAppointment(
                    responsable_appointment=professional,
                    id_appointment=id_appointment,
                    period=period,
                    start_time=start_time,
                    person_id=person_id,
                    service=service
                )
            )
            
            if addUserAppointment["type"] == "DATABASE_ERROR":
                self.response = addUserAppointment
            
            try:
                # Actualizar el documento en la base de datos
                update_result = reservas.update_one(
                    {"fecha": {"$eq": day}},
                    {"$set": {"professionals": professionals}}
                )
            except Exception as e:
                self.response = {
                    "info": f"Error al programar la cita en la base de datos: {e}",
                    "status": "no",
                    "type": "DATABASE_ERROR"  # Tipo de error único
                }

            if not update_result.modified_count > 0:
                self.response = {
                    "info": "Error al programar la cita en la base de datos.",
                    "status": "no",
                    "type": "DATABASE_ERROR"  # Tipo de error único
                }

            self.response = {
                    "info": f"Cita confirmada para {professional} desde {start_time} hasta {end_time}.",
                    "status": "ok",
                    "type": "SUCCESS"  # Tipo de error único
                }
                
        
        self.response = {
            "info": f"No hay disponibilidad para {professional} en el horario solicitado.",
            "status": "no",
            "type": "NO_AVAILABILITY"  # Tipo de error único
        }

