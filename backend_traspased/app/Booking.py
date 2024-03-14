from datetime import datetime, timedelta
import json

# Definición de servicios con su duración y categoría
services = {
    'peinar_con_secador': [timedelta(hours=1), 'peinar_con_secador', 'peluquero'],
    'peinar_recogido': [timedelta(hours=2), 'peinar_recogido', 'peluquero'],
    'montaje_de_mechas': [timedelta(hours=1, minutes=30), 'montaje_de_mechas', 'peluquero'],
    'corte_de_pelo': [timedelta(minutes=30), 'corte_de_pelo', 'peluquero'],
    'corte_y_barba': [timedelta(hours=1), 'corte_y_barba', 'barbero'],
    'pedicura': [timedelta(hours=1), 'pedicura', 'esteticista'],
    'unas': [timedelta(hours=1), 'unas', 'esteticista'],
}


#
peluqueros = ['peluquero_1', 'peluquero_2']
barberos = ['barbero_1', 'barbero_2', 'barbero_3']


# Calendario de disponibilidad para cada profesional en diferentes momentos del día

professionals = {
    'peluquero_1': {
        "morning": {
            "9:00": {"status": "libre"},
            "9:30": {"status":"libre"},
            "10:00": {"status":"libre"},
            "10:30": {"status":"libre"},
            "11:30": {"status":"libre"},
            "12:00": {"status":"libre"},
            "12:30": {"status":"libre"},
            "13:00": {"status":"libre"},
            "13:30": {"status":"libre"},
        },
        "afternoon":{
            "15:00": {"status":"libre"},
            "15:30": {"status":"libre"},
            "16:00": {"status":"libre"},
            "16:30": {"status":"libre"},
            "17:00": {"status":"libre"},
            "17:30": {"status":"libre"},
            "18:00": {"status":"libre"},
            "18:30": {"status":"libre"},
            "19:00": {"status":"libre"},
            "19:30": {"status":"libre"},
            "20:00": {"status":"libre"}
        }
    },
    'peluquero_2': {
        "morning": {
            "9:00": {"status": "libre"},
            "9:30": {"status":"libre"},
            "10:00": {"status":"libre"},
            "10:30": {"status":"libre"},
            "11:30": {"status":"libre"},
            "12:00": {"status":"libre"},
            "12:30": {"status":"libre"},
            "13:00": {"status":"libre"},
            "13:30": {"status":"libre"},
        },
        "afternoon":{
            "15:00": {"status":"libre"},
            "15:30": {"status":"libre"},
            "16:00": {"status":"libre"},
            "16:30": {"status":"libre"},
            "17:00": {"status":"libre"},
            "17:30": {"status":"libre"},
            "18:00": {"status":"libre"},
            "18:30": {"status":"libre"},
            "19:00": {"status":"libre"},
            "19:30": {"status":"libre"},
            "20:00": {"status":"libre"}
        }
    },
    'barbero': {
        "morning": {
            "9:00": {"status": "libre"},
            "9:30": {"status":"libre"},
            "10:00": {"status":"libre"},
            "10:30": {"status":"libre"},
            "11:30": {"status":"libre"},
            "12:00": {"status":"libre"},
            "12:30": {"status":"libre"},
            "13:00": {"status":"libre"},
            "13:30": {"status":"libre"},
        },
        "afternoon":{
            "15:00": {"status":"libre"},
            "15:30": {"status":"libre"},
            "16:00": {"status":"libre"},
            "16:30": {"status":"libre"},
            "17:00": {"status":"libre"},
            "17:30": {"status":"libre"},
            "18:00": {"status":"libre"},
            "18:30": {"status":"libre"},
            "19:00": {"status":"libre"},
            "19:30": {"status":"libre"},
            "20:00": {"status":"libre"}
        }
    },
    'esteticista': {
        "morning": {
            "9:00": {"status": "libre"},
            "9:30": {"status":"libre"},
            "10:00": {"status":"libre"},
            "10:30": {"status":"libre"},
            "11:30": {"status":"libre"},
            "12:00": {"status":"libre"},
            "12:30": {"status":"libre"},
            "13:00": {"status":"libre"},
            "13:30": {"status":"libre"},
        },
        "afternoon":{
            "15:00": {"status":"libre"},
            "15:30": {"status":"libre"},
            "16:00": {"status":"libre"},
            "16:30": {"status":"libre"},
            "17:00": {"status":"libre"},
            "17:30": {"status":"libre"},
            "18:00": {"status":"libre"},
            "18:30": {"status":"libre"},
            "19:00": {"status":"libre"},
            "19:30": {"status":"libre"},
            "20:00": {"status":"libre"}
        }
    },
}

#"info": {
                #    "person_id": "",
                #    "service": "pedicura"
                #   #En las 9:30 esta ocupado ya que la pedicura ocupa 2, 30'
                #}



# Definición de horarios de apertura y cierre
morning_opening_time = datetime.strptime("09:00", '%H:%M')
morning_closing_time = datetime.strptime("13:30", '%H:%M')
afternoon_opening_time = datetime.strptime("15:00", '%H:%M')
afternoon_closing_time = datetime.strptime("20:00", '%H:%M')

def cancel_appointment(professional, period, start_time, service_duration, person_id, service_name):
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

                return f"Cita cancelada para {professional} desde {start_time} hasta {end_datetime.strftime('%H:%M')}."
            else:
                return {
                    "info": "No se puede cancelar la cita porque los detalles de la cita no coinciden.",
                    "status": "no"
                }
        else:
            return {
                "info": f"No hay una cita programada para {professional} a las {start_time}.",
                "status": "no"
            }
    return f"No hay disponibilidad para {professional} en el horario solicitado."

def request_appointment(professional, period, start_time, service_duration, person_id, service):
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


# Ejemplo de solicitud de cita con duración
#   # Puedes ajustar según el servicio

# Primera reserva
result1 = request_appointment(
    professional='peluquero_1', 
    period='afternoon',
    start_time='17:00',
    service_duration=services['peinar_recogido'][0], 
    person_id='10232939',
    service=services['peinar_recogido'][1]
)
print(result1)





result2 = cancel_appointment(
    professional='peluquero_1', 
    period='afternoon',
    start_time='17:00',
    service_duration=services['peinar_recogido'][0], 
    person_id='10232939',
    service_name=services['peinar_recogido'][1]
)
print(result2)
#print(f'\n{professionals["peluquero_1"]["afternoon"]}\n')


result3 = request_appointment(
    professional='peluquero_1', 
    period='afternoon',
    start_time='17:00',
    service_duration=services['montaje_de_mechas'][0], 
    person_id='10232939',
    service=services['montaje_de_mechas'][1]
)
print(result3)

# Ejemplo de cancelación de cita con duración
'''result2 = cancel_appointment(
    professional='peluquero_1', 
    period='afternoon',
    start_time='17:00',
    service_duration=services['peinar_recogido'][0]
)'''
#print(f'\n{json.dump(professionals)}\n')

print(professionals["peluquero_1"])

peluqueros_mas_ocupados = trabajadorMenosOcupado(peluqueros)
print("Peluqueros menos ocupados:", peluqueros_mas_ocupados)


'''
Trabajar en gestion de buscarDisponibilidad encjado con la forma a quien 
añadirle la cita al trabajador con menos ocupación
'''
def buscarDisponibilidad(rama_profesionales, periodo, start_time, service_duration):
    profesionales_menos_ocupados = trabajadorMenosOcupado(rama_profesionales)

    for profesional, _ in profesionales_menos_ocupados:
        resultado = request_appointment(profesional, periodo, start_time, service_duration)
        if resultado["status"] == "ok":
            return resultado

    return {
        "info": "Estan todos ocupados",
        "status": "no"
    }



print(datetime.now())
print(timedelta(hours=1))