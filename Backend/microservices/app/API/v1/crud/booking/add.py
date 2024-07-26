from Backend.microservices.app.API.v1.db.mongodb.database import reservas
from Backend.microservices.app.API.v1.db.mongodb.database import configure
import datetime
from .config import config
import uuid
from crud.users.booking.add import AddBookingUser, AddAppointment
from bson import ObjectId
from pydantic import BaseModel
from datetime import datetime, timedelta

import numpy as np
from numpy import short
import numba as nb

'''
Hace uso de numpy:
- np.array()

Hace uso de numba:
- 
'''

class AddBooking:

    class structure(BaseModel):
        day: int
        month: int
        year: int
        professionals: list
        period: str
        start_time: str
        service_duration: timedelta
        person_id: str
        service: str

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

                day=0,
                month=0,
                year=2024,
                professional="peluquero_2",
                period="afternoon",
                start_time: "17:00",
                service_duration: services['corte_de_pelo'][0],
                person_id: "65ec610288701955b30661a8",
                service: "corte_de_pelo"
            )
        }

        Response = {
            "info": f"Cita confirmada para {professional} desde {start_time} hasta {end_time}.",
            "status": "ok",
            "type": "SUCCESS"  # Tipo de error único
        }
        
        '''

    #@nb.jit(nopython=True)
    def __init__(self, data_raw: structure):
        try:
            self.response = self.buscar_disponibilidad(data_raw)
            print('aq')
            print(self.response)
            
        except Exception as e:
            self.response = {
                "info": f"Error desconocido del servidor: {e}",
                "status": "no",
                "type": "UNKNOWN_ERROR"
            }
            return

    #@nb.jit(nopython=True)
    def buscar_disponibilidad(self, data_raw):
        data = data_raw.model_dump()
        professionals = data["professionals"]

        # Itera sobre los profesionales en orden de menos ocupado a más ocupado
        for professional, _ in professionals:
            resultado = self.add(data_raw, professional)

            print('---->', resultado)
            if resultado["status"] == "ok":
                print('lo conseguio')
                return resultado
                
            elif resultado["status"] == "no" and resultado["type"] == "PROFESSIONAL_BUSSY":
                print('cointunue...')
                continue
            else:
                print('no without->', resultado)
                return resultado

        print('acabo sin anda')
        # Si todos los profesionales están ocupados
        return {
            "info": "Todos los profesionales están ocupados en este momento.",
            "status": "no",
            "type": "NO_AVAILABILITY"
        }
    
    #@nb.jit(nopython=True)
    def add(self, data_raw, professional_selected: str):
        self.response = {}

        try:
            data = data_raw.model_dump()
            day: short = data["day"]
            month: short = data["month"]
            year: short = data["year"]
            professional: str = professional_selected
            period: str = data["period"]
            start_time: str = data["start_time"]
            service_duration: timedelta = data["service_duration"]
            person_id: str = data["person_id"]
            service: str = data["service"]
            #Obtiene la información de la reserva desde la base de datos del día especficado
            day_date = datetime(year, month, day)
            try:
                day_appointment = reservas.find_one({"fecha": {"$eq": day_date}})
            except Exception as e:
                
                self.response = {
                    "info": f"Error al programar la cita en la base de datos: {e}",
                    "status": "no",
                    "type": "DATABASE_ERROR"  # Tipo de error único
                }
                return

            #2services = conversorServices(services_raw)
            professionals = day_appointment.get('professionals')
            print('reservo')


            morning_opening_time = config["morning_opening_time"]
            morning_closing_time = config["morning_closing_time"]
            afternoon_opening_time = config["afternoon_opening_time"]
            afternoon_closing_time = config["afternoon_closing_time"]

            #Verifica si tiene menos de 4 caracteres Ok(09:00) No(9:00)
            if len(start_time) == 4:
                print('len')
                # Si falta algún zero se le añade, se supone que si la hora se queda a 4 caracteres es por la falta de ese 0.
                start_time = "0"+start_time

            # Si realmente no cumple con la longitud de la misma cadena no es una hora
            elif 4 > len(start_time) > 5:
                print('len2')
                return {
                    "info": f"No es una hora valida, por lo visto: {start_time}",
                    "status": "no",
                    "type": "INVALID_HOUR"
                }
            print(start_time)

            start_time_dt = datetime.strptime(start_time, '%H:%M')  # Convertir start_time a datetime
            print(start_time_dt)

            if period == 'morning':
                if start_time_dt < morning_opening_time or start_time_dt >= morning_closing_time:
                    return {
                        "info": "No se puede programar una cita en la mañana fuera del horario de apertura y cierre.",
                        "status": "no",
                        "type": "OUT_TRY_BOOKING"
                    }
            elif period == 'afternoon':
                print(start_time_dt, afternoon_closing_time, '|', start_time_dt, afternoon_opening_time)
                if start_time_dt < afternoon_opening_time or start_time_dt >= afternoon_closing_time:
                    return {
                        "info": "No se puede programar una cita en la tarde fuera del horario de apertura y cierre.",
                        "status": "no",
                        "type": "OUT_TRY_BOOKING"
                    }
                    

            id_appointment = str(uuid.uuid4())
            
            if period not in professionals[professional]:
                return {
                    "info": "El período especificado no es válido para este profesional.",
                    "status": "no",
                    "type": "ERROR1"  # Tipo de error único
                }

            morning_schedule = professionals[professional]['morning']
            last_hour_morning = str(max(morning_schedule.keys(), key=lambda x: datetime.strptime(x, "%H:%M")))
            #print('aqux')
            
            

            if period == 'morning' and start_time >= last_hour_morning:
                print('start_time ->', start_time)
                print('last_hour_morning ->', last_hour_morning)

                print(f'{start_time}, {last_hour_morning} = {start_time >= last_hour_morning}')
                print(f'{period} == "morning", {period == 'morning'}')

                print(start_time >= last_hour_morning)
                return {
                    "info": "No se puede programar una cita en la mañana después del mediodía.",
                    "status": "no",
                    "type": "ERROR2"
                }
            
            
            if period == 'afternoon' and start_time < last_hour_morning:
                return {
                    "info": "No se puede programar una cita en la tarde antes del mediodía.",
                    "status": "no",
                    "type": "ERROR3"
                }
            
            


            '''
            Procurar que sean exactamente igual los valores que se valida la hora,
            deben de ser 5 caracteres, y no 4.
            Esto esta mal -> 9:00
            Esto esta bien -> 09:00
            '''

            if start_time in professionals[professional][period]:

                print(f'EL PROFESSIONAL {professionals[professional]} tiene el {start_time}')
                end_time = (datetime.strptime(start_time, '%H:%M') + service_duration).strftime('%H:%M')

                # Verificar si la cita programada se extiende más allá del horario de cierre de la mañana o tarde
                if period == 'morning' and datetime.strptime(end_time, '%H:%M') > morning_closing_time:
                    return {
                        "info": f"No se puede programar la cita para {professional} después del horario de cierre de la mañana.",
                        "status": "no",
                        "type": "OUT_SCHULDE_BEFORE_MORNING"  # Tipo de error único
                    }
                elif period == 'afternoon' and datetime.strptime(end_time, '%H:%M') > afternoon_closing_time:
                    return {
                        "info": f"No se puede programar la cita para {professional} después del horario de cierre de la tarde.",
                        "status": "no",
                        "type": "OUT_SCHULDE_AFTER_AFTERNOON"  # Tipo de error único
                    }

                available_slots = np.array(list(professionals[professional][period].items()))
                #available_slots = set(professionals[professional][period].keys())

                
                # Verificar si algún intervalo parcial está disponible
                start_datetime = datetime.strptime(start_time, '%H:%M')
                end_datetime = datetime.strptime(end_time, '%H:%M')
                
                overlapping_slots = [
                                        (slot, status) for slot, status in available_slots
                                        
                                        if start_datetime < datetime.strptime(slot, '%H:%M') < end_datetime
                                            or start_datetime <= datetime.strptime(slot, '%H:%M') < end_datetime
                                    ]
                
                print('reservo')
                # Verificar si hay algún solapamiento en la franja horaria
                if overlapping_slots and any(status["status"] == 'ocupado' for _, status in overlapping_slots):
                    print('entro')
                    return {
                        "info": f"No se puede programar la cita para {professional} en la franja horaria solicitada.",
                        "status": "no",
                        "type": "PROFESSIONAL_BUSSY"  # Tipo de error único
                    }
                    print('add self.response->', self.response)
                    

                print('asd')
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

                
                print('pro ->', professional)
                dataUserAppointment = AddAppointment(
                    day=day,
                    month=month,
                    year=year,
                    responsable_appointment=professional,
                    id_appointment=id_appointment,
                    period=period,
                    start_time=start_time,
                    person_id=person_id,
                    service=service
                )

                addUserAppointment = AddBookingUser(dataUserAppointment)

                if addUserAppointment.response and addUserAppointment.response["type"] == "DATABASE_ERROR":
                    return addUserAppointment

                
                try:
                    # Actualizar el documento en la base de datos
                    update_result = reservas.update_one(
                        {"fecha": {"$eq": day_date}},
                        {"$set": {"professionals": professionals}}
                    )
                except Exception as e:
                    return {
                        "info": f"Error al programar la cita en la base de datos: {e}",
                        "status": "no",
                        "type": "DATABASE_ERROR"  # Tipo de error único
                    }

                if not update_result.modified_count > 0:
                    return {
                        "info": "Error al programar la cita en la base de datos.",
                        "status": "no",
                        "type": "DATABASE_ERROR"  # Tipo de error único
                    }

                print('reservo')
                return {
                    "info": f"Cita confirmada para {professional} desde {start_time} hasta {end_time}.",
                    "status": "ok",
                    "type": "SUCCESS"  # Tipo de error único
                }
            else:
               
                return {
                    "info": f"No hay disponibilidad para {professional} en el horario solicitado.",
                    "status": "no",
                    "type": "NO_AVAILABILITY"  # Tipo de error único
                }
            
        except Exception as e:
            self.response = {
                "info": f"Error desconocido del servidor: {e}",
                "status": "no",
                "type": "UNKNOW_ERROR"
            }