from datetime import time, datetime, timedelta 

'''
# Crear una hora específica
hora_inicial = time(hour=9, minute=0)

# Sumar 2 horas
hora_final = (datetime.combine(datetime.today(), hora_inicial) + timedelta(hours=2)).time()
print(f"Hora final: {hora_final.strftime('%H:%M')}")

# Restar 30 minutos
hora_resta = (datetime.combine(datetime.today(), hora_inicial) - timedelta(minutes=30)).time()
print(f"Hora con resta: {hora_resta.strftime('%H:%M')}")

print(datetime.today())
print('\n\n\n')
'''



services = {
    'peinar_con_secador': [
        timedelta(hours=1),
        'peinar_con_secador',
        'peluquero'
    ],
    'peinar_recogido': [
        timedelta(hours=2),
        'peinar_recogido',
        'peluquero'
    ],
    'montaje_de_mechas': [
        timedelta(hours=1, minutes=30),
        'montaje_de_mechas',
        'peluquero'
    ],
    'corte_de_pelo': [
        timedelta(minutes=30),
        'corte_de_pelo',
        'peluquero'
    ],
    'corte_y_barba': [
        timedelta(hours=1),
        'corte_y_barba',
        'barbero'
    ],
    'pedicura': [
        timedelta(hours=1),
        'pedicura',
        'esteticista'
    ],
    'unas': [
        timedelta(hours=1),
        'unas',
        'esteticista'
    ],
}


'''
Tendran en la reservas_personal, por cada miembro las horas reservadas
en forma de lista dentro de una lista padre

Todo esto es se va a guardar en el dia correspondiente, y esto es una
prueba, ya que se reservas_personal, se obtendra de la base de datos en
mongodb del dia.

reservas_personal = {
    "peluquero_1": [
        [
            "15:00",  //Hora de la cita reservada (hora_del_dia:minutos)
            "1:00:00",  //Duracion del servicio (horas:minutos:segundos)
            "corte_de_pelo",  //Tipo de servicio
        ]
    ]
}
'''

#Prueba
reservas_personal = {
    "peluquero_1": [
        
        [
            "16:00",
            "1:00:00",
            "peinar_con_secador"
        ],
        [
            "17:00",
            "1:00:00",
            "peinar_con_secador"
        ]
        
        
    ],
    "peluquero_2": [
        [
            "15:00",
            "1:00:00",
            "corte_de_pelo"
        ],
    ],
    "barbero": [

    ],
    "esteticista": [

    ]
}




#Comprobara los 2
def reservas_indisponibles_peluquero():
    global reservas_personal

    unavailable_hours = [
        [],
        []
    ]

    def extraccion_de_reservas_indisponibles():
        pass
    '''
    Retornara un array con entre las horas no disponibles
    al validar_hora(), de cada peluquero
    '''
    
    print('1-------------------------------------------1')

    for reservas_hechas in reservas_personal["peluquero_1"]:
        print('\n')

        hora_cita_inicio = datetime.strptime(reservas_hechas[0], "%H:%M")
        duracion_servicio = datetime.strptime(reservas_hechas[1], "%H:%M:%S").time()

        duracion_timedelta = timedelta(
            hours=duracion_servicio.hour,
            minutes=duracion_servicio.minute
        )

        hora_cita_fin = hora_cita_inicio + duracion_timedelta

        print(f'Hora de la cita: {hora_cita_inicio.strftime("%H:%M")}')
        print(f'Duración del servicio: {str(duracion_timedelta)}')
        print(f'Hora de finalización de la cita: {hora_cita_fin.strftime("%H:%M")}')
        print(f'Tipo de servicio: {reservas_hechas[2]}')
        print('\n')

        unavailable_hours[0].append([
            hora_cita_inicio.strftime("%H:%M"),
            hora_cita_fin.strftime("%H:%M")

        ])

        


    print('1-------------------------------------------1\n')
    print('2-------------------------------------------2')

    for reservas_hechas in reservas_personal["peluquero_2"]:
        print('\n')

        hora_cita_inicio = datetime.strptime(reservas_hechas[0], "%H:%M")
        duracion_servicio = datetime.strptime(reservas_hechas[1], "%H:%M:%S").time()

        duracion_timedelta = timedelta(
            hours=duracion_servicio.hour,
            minutes=duracion_servicio.minute
        )

        hora_cita_fin = hora_cita_inicio + duracion_timedelta

        print(f'Hora de la cita: {hora_cita_inicio.strftime("%H:%M")}')
        print(f'Duración del servicio: {str(duracion_timedelta)}')
        print(f'Hora de finalización de la cita: {hora_cita_fin.strftime("%H:%M")}')
        print(f'Tipo de servicio: {reservas_hechas[2]}')
        print('\n')

        unavailable_hours[1].append([
            hora_cita_inicio.strftime("%H:%M"),
            hora_cita_fin.strftime("%H:%M")

        ])
    
    return unavailable_hours


def reservas_indisponibles_otros(name_personal):
    global reservas_personal

    '''
    Bale por cada reserva extraemos el inicio de la cita
    y con una variable nueva añadimos con la duracion y nos
    saldra el fin de la cita, al verificar y da problemas al
    obtener porque es la hora que se acaba la cita, lo ignoraremos
    '''


    for reservas_hechas in reservas_personal[name_personal]:
        print(reservas_hechas[0])

        
    




def validar_hora(
        hora_validar, 
        
        hora_inicio_morning, 
        hora_fin_morning, 
         
        hora_inicio_afternoon, 
        hora_fin_afternoon,

        service,
    ):

    #Datos en sucio, todos los datos de tiempo
    hora_inicio_morning = datetime.strptime(hora_inicio_morning, "%H:%M").time()
    hora_fin_morning = datetime.strptime(hora_fin_morning, "%H:%M").time()
    
    hora_inicio_afternoon = datetime.strptime(hora_inicio_afternoon, "%H:%M").time()
    hora_fin_afternoon = datetime.strptime(hora_fin_afternoon, "%H:%M").time()
    
    validate = datetime.strptime(hora_validar, "%H:%M").time()



    #   Saber cuando acaba la cita & se validara si es posible en el
    #   horario, juntando el tiempo a transcurrir y la hora del dia,
    #   dando como resultado la hora del dia transcurrido por el tiempo determinado
    
    validate_datetime = datetime.combine(datetime.today(), validate)
    validate_reserva = (validate_datetime + service[0]).time()
    print(f'Acabara a las: {validate_reserva.strftime("%H:%M")}')



    #Mirar el personal las horas libres en trabajo
    '''
    Debera obtener todas las citas pendientes y entre la hora 
    prevista de la cita y en la hora que debera acabar no pueda
    reservar en esas horas por ejemplo

    En el caso de los peluqueros como son 2 deberemos escojer
    y comprobar que tengan el horario libre si uno lo añade. Pero
    debera compensarse
    '''
    
    
    if service[2] == 'peluquero':
        horas_indis = reservas_indisponibles_peluquero()
        print(horas_indis)
    else:
        horas_indis = reservas_indisponibles_otros(service[2])
        print(horas_indis)
    

    def validacion_horas_indisponibles(personas_indisponible):
        

        for i, persona_indisponible in enumerate(personas_indisponible):
            print(f'----peluquero_{i + 1}----')

            for horas_indisponibles in persona_indisponible:
                hora_indis_start = datetime.strptime(horas_indisponibles[0], "%H:%M").time()
                hora_indis_end = datetime.strptime(horas_indisponibles[1], "%H:%M").time()

                # Verificar solapamiento
                print(f'{hora_indis_start} - {hora_indis_end}')
                print(f'{validate} - {validate_reserva}\n')
                print(validate <= hora_indis_start <= validate_reserva)
                print(validate <= hora_indis_end <= validate_reserva)
                if (
                    #
                    validate <= hora_indis_start <= validate_reserva or
                    validate <= hora_indis_end <= validate_reserva
                ):
                    print('Verificado que hay una hora cerca')

                    if hora_indis_start <= validate <= hora_indis_end:
                        print('En la hora que pidio el cliente esta vacio')

                        if not hora_indis_start <= validate_reserva <= hora_indis_end:
                            print('En la hora que pidio el cliente esta vacio al acabar la cita')


    '''
    Debemos que la cita que pide el cliente en esa hora hay algo
    Esto significa que si valida 15:00 que es la primera cita dle registro
    y pides cita a las 17:00, claramente
    te la dara porque valida si esta ocupado o no. Si que tenemos
    que ver si la cita que pide el cliente y en el final que acaba
    tiene entre medio una cita ocupada 

    '''
            




    # Luego, puedes usar esta función para validar la disponibilidad de la hora.
    validate = datetime.strptime("15:30", "%H:%M").time()  # Reemplaza con la hora que necesitas validar
    validate_reserva = (datetime.combine(datetime.today(), validate) + timedelta(hours=1)).time()  # Reemplaza con la duración del servicio

    eleccion_de_persona = validacion_horas_indisponibles(horas_indis)
    if eleccion_de_persona:
        print(f'La hora no está disponible. {eleccion_de_persona}')
    else:
        print('La hora está disponible.')

    


    if hora_inicio_morning <= validate_reserva <= hora_fin_morning:
        print(f'Se reservo por la mañana: {service[1]} a las {hora_validar}h')

    elif hora_inicio_afternoon <= validate_reserva <= hora_fin_afternoon:
        print(f'Se reservo por la tarde: {service[1]} a las {hora_validar}h')

    else:
        print(f'No hay hora para: {service[1]}')







# Debe tener el mínimo
print('\n\n\n')

'''
No se contara el domingo, y debera
hacer una plantilla exclusiva para el sabado.
Bueno deberemos de hacer 2 plantillas en dias, laborales y el sabado

Recordar que dias esta cerrado la peluqueria
y hacer otro sistema para eso.
'''

'''
Sistema de recomendaciones, una hora mas cercana o la siguiente que
tenga
'''

horario_peluqueria = {
    "morning": {
        "start": "9:00",
        "end": "13:30"
    },
    "afternoon": {
        "start": "15:00",
        "end": "20:00"
    }
}

data = {
    "hora_validar": "16:30",
    "hora_inicio_morning": horario_peluqueria["morning"]["start"],
    "hora_fin_morning": horario_peluqueria["morning"]["end"],
    "hora_inicio_afternoon": horario_peluqueria["afternoon"]["start"],
    "hora_fin_afternoon": horario_peluqueria["afternoon"]["end"],
    "service": services["peinar_con_secador"]
}

validar_hora(
    hora_validar= data["hora_validar"],
    hora_inicio_morning= data["hora_inicio_morning"],
    hora_fin_morning= data["hora_fin_morning"],
    hora_inicio_afternoon= data["hora_inicio_afternoon"],
    hora_fin_afternoon= data["hora_fin_afternoon"],
    service= data["service"] #(Reicibiria la info del servicio)
)
print('\n\n')