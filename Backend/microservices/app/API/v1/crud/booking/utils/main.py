from datetime import timedelta

def conversorServices(services_raw):

    '''
    Convierte los servicios guardados en la DB, en una lista para ser usadas
    Example:
    - services_raw = configure.find_one({ "_id": ObjectId("65ec5f9f88701955b30661a5") })
    '''

    dict_services = {}

    for service in services_raw['services']:
        service_name = service['nombre']

        '''
        Verifica que una cita no sobrepase de las 4 horas, así elaborare una partado de la app
        para contactar especialmente al admin para que pueda así pueda decidir que hacer
        '''
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




#services = conversorServices(services_raw)