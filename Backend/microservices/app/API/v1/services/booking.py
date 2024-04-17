from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import json
import uuid
from bson import ObjectId
from pprint import pprint



from Backend.microservices.app.API.v1.db.database import reservas
from Backend.microservices.app.API.v1.db.database import users
from Backend.microservices.app.API.v1.db.database import configure

from datetime import datetime


# Fecha de Python para comparar
fecha_python = datetime(2024, 3, 26)
res = reservas.find_one({"fecha": {"$eq": fecha_python}})
services_raw = configure.find_one({ "_id": ObjectId("65ec5f9f88701955b30661a5") })


dict_services = {}

from datetime import timedelta

def conversorServices(services_raw):
    dict_services = {}

    for service in services_raw['services']:
        service_name = service['nombre']

        
        #Verifica si las horas no superan de las 4 horas, y si en los minutos son de 0 o 30 minutos
        verify_hour = service['duracion']['horas'] >= 0 and service['duracion']['horas'] <= 4
        verify_minutes = service['duracion']['minutos'] == 0 or service['duracion']['minutos'] == 30

        if verify_hour and verify_minutes:
            duration = timedelta(hours=service['duracion']['horas'], minutes=service['duracion']['minutos'])
            service_type = service['tipo']
            dict_services[service_name] = [duration, service_name, service_type]
        else:
            if not verify_hour:
                print('La hora no es aceptable para el servicio:', service_name)
            if not verify_minutes:
                print('Los minutos deben ser 0 o 30 minutos para el servicio:', service_name)
    
    #pprint(dict_services)
    return dict_services

services = conversorServices(services_raw)


'''
personal: {
    peluqueros: [
        'peluquero_1',
        'peluquero_2'
    ],
    barberos: [
        'barbero_1',
        'barbero_2',
        'barbero_3'
    ],
    esteticistas: [
        'esteticista_1',
        'esteticista_2',
        'esteticista_3'
    ]
}

services: {
    peluqueros: {
        corte_de_pelo,
        montaje_de_mechas,
        peinar_recogido,
        peinar_con_secador
    },
    barberos: {
        corte_y_barba,
        
    }
}
'''

peluqueros = ['peluquero_1', 'peluquero_2']
barberos = ['barbero_1', 'barbero_2', 'barbero_3']
esteticistas = ['esteticista_1', 'esteticista_2', 'esteticista_3']

professionals = res.get('professionals')
#print(professionals)

'''
Example Appointment Done it:
###########################
'17:00': {
      'status':'ocupado', 
      'info': {
        'person_id': '10232939',
        'service': 'montaje_de_mechas'
      }
      
    },
###########################
'''



# Definición de horarios de apertura y cierre
morning_opening_time = datetime.strptime("09:00", '%H:%M')
morning_closing_time = datetime.strptime("13:30", '%H:%M')
afternoon_opening_time = datetime.strptime("15:00", '%H:%M')
afternoon_closing_time = datetime.strptime("20:00", '%H:%M')

def cancel_appointment(professional, period, start_time, service_duration, person_id, service_name, id_appointment):
    start_time_dt = datetime.strptime(start_time, '%H:%M')  # Convertir start_time a datetime

    if period == 'morning':
        if start_time_dt < morning_opening_time or start_time_dt >= morning_closing_time:
            return {
                "info": "No se puede cancelar una cita en la mañana fuera del horario de apertura y cierre.",
                "status": "no"
            }
    elif period == 'afternoon':
        if start_time_dt < afternoon_opening_time or start_time_dt >= afternoon_closing_time:
            return {
                "info": "No se puede cancelar una cita en la tarde fuera del horario de apertura y cierre.",
                "status": "no"
            }

    if start_time in professionals[professional][period]:
        if "info" in professionals[professional][period][start_time]:
            info = professionals[professional][period][start_time]["info"]
            if info["service"] == service_name and info["person_id"] == person_id:
                start_datetime = datetime.strptime(start_time, '%H:%M')
                end_datetime = start_datetime + service_duration

                # Marcar todas las franjas horarias asociadas a la cita como "libres"
                while start_datetime < end_datetime:
                    current_time = start_datetime.strftime('%H:%M')
                    professionals[professional][period][current_time].pop("info", None)  # Remover la información de la cita
                    professionals[professional][period][current_time]["status"] = 'libre'
                    start_datetime += timedelta(minutes=30)


                userRemoveAppointment = BookingUser.remove(
                    id_appointment=id_appointment,
                    person_id=person_id
                )

                if userRemoveAppointment["type"] == "DATABASE_ERROR":
                    return userRemoveAppointment
                
                # Actualizar el documento en la base de datos
                update_result = reservas.update_one(
                    {"fecha": {"$eq": fecha_python}},
                    {"$set": {"professionals": professionals}}
                )

                if update_result.modified_count > 0:
                    # El tipo de error es "SUCCESS" indicando que la operación se realizó correctamente
                    return {"info": f"Cita cancelada para {professional} desde {start_time} hasta {end_datetime.strftime('%H:%M')}.", "status": "success", "type": "SUCCESS"}
                else:
                    # El tipo de error es "DATABASE_ERROR" indicando que hubo un error al actualizar la base de datos
                    return {"info": "Error al cancelar la cita en la base de datos.", "status": "error", "type": "DATABASE_ERROR"}
            else:
                # El tipo de error es "MISMATCH" indicando que los detalles de la cita no coinciden
                return {"info": "No se puede cancelar la cita porque los detalles de la cita no coinciden.", "status": "error", "type": "MISMATCH"}
        else:
            # El tipo de error es "NO_APPOINTMENT" indicando que no hay una cita programada en el horario especificado
            return {"info": f"No hay una cita programada para {professional} a las {start_time}.", "status": "error", "type": "NO_APPOINTMENT"}
    return {"info": f"No hay disponibilidad para {professional} en el horario solicitado.", "status": "error", "type": "NO_AVAILABILITY"}



def request_appointment(professional, period, start_time, service_duration, person_id, service):

    start_time_dt = datetime.strptime(start_time, '%H:%M')  # Convertir start_time a datetime

    if period == 'morning':
        if start_time_dt < morning_opening_time or start_time_dt >= morning_closing_time:
            return {
                "info": "No se puede programar una cita en la mañana fuera del horario de apertura y cierre.",
                "status": "no"
            }
    elif period == 'afternoon':
        if start_time_dt < afternoon_opening_time or start_time_dt >= afternoon_closing_time:
            return {
                "info": "No se puede programar una cita en la tarde fuera del horario de apertura y cierre.",
                "status": "no"
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
    
    if period == 'morning' and start_time >= last_hour_morning:
        return {
            "info": "No se puede programar una cita en la mañana después del mediodía.",
            "status": "no",
            "type": "ERROR2"  # Tipo de error único
        }
    elif period == 'afternoon' and start_time < last_hour_morning:
        return {
            "info": "No se puede programar una cita en la tarde antes del mediodía.",
            "status": "no",
            "type": "ERROR3"  # Tipo de error único
        }

    if start_time in professionals[professional][period]:
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
            return {
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

        

        addUserAppointment = BookingUser.add(
            responsable_appointment=professional,
            id_appointment=id_appointment,
            period=period,
            start_time=start_time,
            person_id=person_id,
            service=service
        )
        
        if addUserAppointment["type"] == "DATABASE_ERROR":
            return addUserAppointment
        
        # Actualizar el documento en la base de datos
        update_result = reservas.update_one(
            {"fecha": {"$eq": fecha_python}},
            {"$set": {"professionals": professionals}}
        )

        if update_result.modified_count > 0:
            return {
                "info": f"Cita confirmada para {professional} desde {start_time} hasta {end_time}.",
                "status": "ok",
                "type": "SUCCESS"  # Tipo de error único
            }
        else:
            return {
                "info": "Error al programar la cita en la base de datos.",
                "status": "no",
                "type": "DATABASE_ERROR"  # Tipo de error único
            }
    
    return {
        "info": f"No hay disponibilidad para {professional} en el horario solicitado.",
        "status": "no",
        "type": "NO_AVAILABILITY"  # Tipo de error único
    }




'''def request_appointment(professional, period, start_time, service_duration, person_id, service):
    if start_time in professionals[professional][period]:
        end_time = (datetime.strptime(start_time, '%H:%M') + service_duration).strftime('%H:%M')

        # Verificar si la cita programada se extiende más allá del horario de cierre de la mañana o tarde
        if period == 'morning':
            if datetime.strptime(end_time, '%H:%M') > morning_closing_time:
                return {
                    "info": f"No se puede programar la cita para {professional} después del horario de cierre de la mañana.",
                    "status": "no"
                }
        elif period == 'afternoon':
            if datetime.strptime(end_time, '%H:%M') > afternoon_closing_time:
                return {
                    "info": f"No se puede programar la cita para {professional} después del horario de cierre de la tarde.",
                    "status": "no"
                }

        available_slots = list(professionals[professional][period].items())
        
        # Verificar si algún intervalo parcial está disponible
        start_datetime = datetime.strptime(start_time, '%H:%M')
        end_datetime = datetime.strptime(end_time, '%H:%M')
        
        overlapping_slots = [(slot, status) for slot, status in available_slots
                             if start_datetime < datetime.strptime(slot, '%H:%M') < end_datetime
                             or start_datetime <= datetime.strptime(slot, '%H:%M') < end_datetime]

        # Verificar si hay algún solapamiento en la franja horaria
        if overlapping_slots and any(status["status"] == 'ocupado' for _, status in overlapping_slots):
            return {
                "info": f"No se puede programar la cita para {professional} en la franja horaria solicitada.",
                "status": "no"
            }

        # Marcar el intervalo parcial como ocupado y guardar la información de la cita
        for slot, _ in available_slots:
            if start_datetime <= datetime.strptime(slot, '%H:%M') < end_datetime:
                professionals[professional][period][slot] = {
                    "status": 'ocupado',
                    "info": {
                        "person_id": person_id,
                        "service": service
                    }
                }
                if slot != start_time:  # Solo limpiar 'info' en las franjas horarias distintas a la seleccionada
                    professionals[professional][period][slot].pop("info", None)
                
        return {
            "info": f"Cita confirmada para {professional} desde {start_time} hasta {end_time}.",
            "status": "ok"
        }
    
    return {
        "info": f"No hay disponibilidad para {professional} en el horario solicitado.",
        "status": "no"
    }
'''

def trabajadorMenosOcupado(rama_profesionales):
    ocupacion_profesionales = []

    for profesional in rama_profesionales:
        contador_ocupado = 0
        for periodo in professionals[profesional]:
            for hora, estado in professionals[profesional][periodo].items():
                if estado["status"] == "ocupado":
                    contador_ocupado += 1
        ocupacion_profesionales.append((profesional, f"{contador_ocupado/2}h")) #Se divide en 2, porque hacemos uso de 30', y tendremos una hora por 2 medias horas

    ocupacion_profesionales.sort(key=lambda x: x[1])

    return ocupacion_profesionales





'''
Trabajar en gestion de buscarDisponibilidad encjado con la forma a quien 
añadirle la cita al trabajador con menos ocupación
'''
import json

def buscarDisponibilidad(rama_profesionales, period, start_time, service_duration, person_id, service):
    """
    Esta función busca la disponibilidad entre los profesionales menos ocupados para programar una cita.
    
    Parameters:
        rama_profesionales (dict): Diccionario que contiene información sobre los profesionales y sus horarios.
        period (str): Periodo del día en el que se desea programar la cita (mañana o tarde).
        start_time (str): Hora de inicio deseada para la cita.
        service_duration (datetime.timedelta): Duración del servicio.
        person_id (str): Identificador de la persona que solicita la cita.
        service (str): Tipo de servicio solicitado.
    
    Returns:
        dict: Un diccionario que contiene información sobre el resultado de la búsqueda de disponibilidad.
            Si se encuentra un profesional disponible, devuelve información sobre la cita programada.
            Si todos los profesionales están ocupados, devuelve un mensaje indicando la falta de disponibilidad.
    """
    profesionales_menos_ocupados = trabajadorMenosOcupado(rama_profesionales)

    for profesional, _ in profesionales_menos_ocupados:
        
        resultado = request_appointment(profesional, period, start_time, service_duration, person_id, service)

        if resultado["status"] == "ok":
            return resultado
        elif resultado["type"] == "DATABASE_ERROR":

            return resultado
        elif resultado["status"] == "no":
            return {
                "info": "Todos los profesionales están ocupados en este momento.",
                "status": "no",
                "type": "NO_AVAILABILITY" 
            }
        
    return {
        "info": "Todos los profesionales están ocupados en este momento.",
        "status": "no",
        "type": "NO_AVAILABILITY"  # Tipo de error único
    }



#El código proporcionado parece estar bien estructurado para la lógica de reserva de citas. Para implementar la función addBookingUser, puedes seguir el mismo enfoque que sugerí anteriormente. Aquí está cómo podrías hacerlo:
#python

class BookingUser:
    @staticmethod
    def add(
        responsable_appointment,  # Persona que realiza su cita
        id_appointment,
        period,
        start_time,
        person_id,
        service
    ):
        # Encuentra al usuario
        user = users.find_one({ "_id": ObjectId(person_id) })

        if user:
            # Define los datos de la reserva
            booking_data = {
                "service": service,
                "period": period,
                "start_time": start_time,
                "responsable_appointment": responsable_appointment,
                "date_appointment": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            }

            # Actualiza el usuario con la nueva reserva
            update_result = users.update_one(
                { "_id": ObjectId(person_id) },
                { "$set": { f"reservas.{id_appointment}": booking_data } }
            )

            if update_result.modified_count > 0:
                return {
                    "info": f"Reserva agregada al usuario {person_id}.",
                    "status": "ok",
                    "type": "SUCCESS"  # Tipo de éxito
                }
            else:
                return {
                    "info": "Error al agregar reserva al usuario.",
                    "status": "no",
                    "type": "DATABASE_ERROR"  # Tipo de error de base de datos
                }
        else:
            return {
                "info": "Usuario no encontrado en la base de datos.",
                "status": "no",
                "type": "DATABASE_ERROR"  # Tipo de error de base de datos
            }



    @staticmethod
    def remove(
        id_appointment,
        person_id
    ):
        # Actualiza el documento para eliminar la propiedad 'reservas' con el ID específico
        update_result = users.update_one(
            { "_id": ObjectId(person_id) },
            { "$unset": { f"reservas.{id_appointment}": "" } }
        )

        # Verifica si la operación se realizó correctamente
        if update_result.modified_count > 0:
            return {
                "info": f"Se eliminó correctamente la reserva con ID {id_appointment} del usuario con ID {person_id}.",
                "status": "ok"
            }
        else:
            return {
                "info": f"No se encontró la reserva con ID {id_appointment} en el usuario con ID {person_id}.",
                "status": "no",
                "type": "MISMATCH"  # Tipo de error único
            }    

'''

Antes ejecutar las funciones apra saber el mejor empleado para hacer la cita y 

result3 = cancel_appointment(
    professional="peluquero_1", 
    period='afternoon',
    start_time='15:00',
    service_duration=services['corte_de_pelo'][0], 
    person_id='65562cb12eca8eac9e65680a',
    service_name=services['corte_de_pelo'][1],
    id_appointment='784acb19-5621-4c7a-930e-b4b97107eabf'
)
print(result3)'''




'''
  🚧 🚧 🚧 🚧 🚧

· Aplicar si la misma persona ya tiene una cita en ese horario
  no poder añadirle otra cita, y si quiere cambiarla, primero eliminar la que tiene

  Comprovará en las "reservas" de su perfil de usuario si ya tiene cita, si tiene cita
  no poder hacer otra cita, no lo permitirá.

  Pero cuando quiera pedir otra cita y ya paso se quita esa cita ya hecha y luego le 
  da permiso a hacer otra cita.

  A paritr de su id_appointment, se la quita del usuario y se cancela la cita, pero con
  el otro uso de quitar la cita luego de haberlo hecho. Se puede quitar intencionadamente,
  pero también cuando ya acabo la cita
'''

result4 = buscarDisponibilidad(
    rama_profesionales=peluqueros, 
    period='afternoon',
    start_time='7:00',
    service_duration=services['corte_de_pelo'][0], 
    person_id='65ec610288701955b30661a8',
    service='corte_de_pelo'
)


print("\n", "\n", result4, "\n", "\n")

