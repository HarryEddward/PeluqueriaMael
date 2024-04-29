from db.database import users, reservas
from pydantic import BaseModel
from datetime import datetime, timedelta
from .config import config
from crud.users.booking.remove import RemoveBookingUser

from crud.booking.utils.verifyUserAppointment import verifyUserAppointment

class  RemoveBooking:



    class structure(BaseModel):
        day: int
        month: int
        year: int
        professional: str
        period: str
        start_time: str
        service_duration: timedelta
        person_id: str
        service_name: str
        id_appointment: str


    def __init__(self, data_raw: structure) -> None:
        self.response = None
        try:
            data = data_raw.model_dump()
            self.response = self.remove(
                day= data["day"],
                month= data["month"],
                year= data["year"],
                professional= data["professional"],
                period= data["period"],
                start_time= data["start_time"],
                service_duration= data["service_duration"],
                person_id= data["person_id"],
                service_name= data["service_name"], 
                id_appointment= data["id_appointment"]
            )
        except Exception as e:
            self.response = {
                "info": f"Error desconocido del servidor: {e}",
                "status": "no",
                "type": "UNKNOW_ERROR"
            }

    def remove(self, day, month, year, professional, period, start_time, service_duration, person_id, service_name, id_appointment) -> dict:
        start_time_dt = datetime.strptime(start_time, '%H:%M')  # Convertir start_time a datetime
        print('aqui?')
        try:
            #print(year, month, day)
            day_date = datetime(year, month, day)
            day_appointment = reservas.find_one({"fecha": {"$eq": day_date}})
            #print('day_appointment ->', day_appointment)
            professionals = day_appointment.get('professionals')
        except Exception as e:
            return {
                "info": f"Error al acceder a la base de datos: {e}",
                "status": "no",
                "type": "DATABASE_ERROR"
            }

        print('alla')
        morning_opening_time = config["morning_opening_time"]
        morning_closing_time = config["morning_closing_time"]
        afternoon_opening_time = config["afternoon_opening_time"]
        afternoon_closing_time = config["afternoon_closing_time"]
        print('asa')
        if period == 'morning':
            if start_time_dt < morning_opening_time or start_time_dt >= morning_closing_time:
                return {
                    "info": "No se puede cancelar una cita en la mañana fuera del horario de apertura y cierre.",
                    "status": "no",
                    "type": "OUT_BOOKING"
                }
        elif period == 'afternoon':
            if start_time_dt < afternoon_opening_time or start_time_dt >= afternoon_closing_time:
                return {
                    "info": "No se puede cancelar una cita en la tarde fuera del horario de apertura y cierre.",
                    "status": "no",
                    "type": "OUT_BOOKING"
                }
        print('llega aqui')
        print(professionals[professional][period])
        
        if start_time in professionals[professional][period]:
            
            #print(professionals[professional][period][start_time])
            
            #Recorrer por cada franja de horario que tiene el personal y verifica si tiene info, si lo tiene es porque hay una cita reservada
            if "info" in professionals[professional][period][start_time]:
                info = professionals[professional][period][start_time]["info"]

                #Verifica si el servicio coincide con el usuario hecho
                if info["service"] == service_name and info["person_id"] == person_id:
                    start_datetime = datetime.strptime(start_time, '%H:%M')
                    end_datetime = start_datetime + service_duration

                    # Marcar todas las franjas horarias asociadas a la cita como "libres"
                    while start_datetime < end_datetime:
                        current_time = start_datetime.strftime('%H:%M')
                        print(current_time)
                        professionals[professional][period][current_time].pop("info", None)  # Remover la información de la cita
                        professionals[professional][period][current_time]["status"] = 'libre'
                        start_datetime += timedelta(minutes=30)

                    print(professionals)

                    # Verifica si intenta cancelar la cita  antes de los 3 días de realizarlo
                    # Code...
                    today_date = datetime.now().date()
                    verify_date = day_date - today_date
                    

                    #Aún para testear
                    if verify_date.days < 3:
                        return {
                            "info": "Faltan menos de 3 dias para la reserva, y no se puede eliminarla",
                            "status": "no",
                            "type": "UNAUTHORIZED_APPOINTMENT_CANCELLATION"
                        }

                    # Actualizar el documento en la base de datos
                    update_result = reservas.update_one(
                        {"fecha": {"$eq": day_date}},
                        {"$set": {"professionals": professionals}}
                    )

                    userRemoveAppointment = RemoveBookingUser(
                        RemoveBookingUser.structure(
                            id_appointment=id_appointment,
                            person_id=person_id
                        )
                        
                    )

                    if not userRemoveAppointment.response["status"] == 'ok':
                        print('pasa algo en la db user remove')
                        return userRemoveAppointment.response
                    
                    

                    if update_result.modified_count > 0:
                        # El tipo de error es "SUCCESS" indicando que la operación se realizó correctamente
                        return {"info": f"Cita cancelada para {professional} desde {start_time} hasta {end_datetime.strftime('%H:%M')}.", "status": "ok", "type": "SUCCESS"}
                    else:
                        # El tipo de error es "DATABASE_ERROR" indicando que hubo un error al actualizar la base de datos
                        return {"info": "Error al cancelar la cita en la base de datos.", "status": "no", "type": "DATABASE_ERROR"}
                else:
                    # El tipo de error es "MISMATCH" indicando que los detalles de la cita no coinciden
                    return {"info": "No se puede cancelar la cita porque los detalles de la cita no coinciden.", "status": "no", "type": "MISMATCH"}
            else:
                # El tipo de error es "NO_APPOINTMENT" indicando que no hay una cita programada en el horario especificado
                return {"info": f"No hay una cita programada para {professional} a las {start_time}.", "status": "no", "type": "NO_APPOINTMENT"}
        return {"info": f"No hay disponibilidad para {professional} en el horario solicitado.", "status": "no", "type": "NO_AVAILABILITY"}

