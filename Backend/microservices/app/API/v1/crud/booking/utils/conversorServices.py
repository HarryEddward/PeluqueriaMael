from pydantic import BaseModel
from datetime import timedelta

from db.database import configure
from bson import ObjectId

class conversorServices:
    '''
    SI -> Obtiene todos los servicios guardados en cofiguración
    NO -> Obtiene el id de configruation db de la coleccion y leugo devuelve todo el personal en difernetes
    arrays
    '''

    '''
    Que quiero hacer?
    Quiero que obtenga la version de la ficha del dia a reservar, y pase la version para que obtenga, devolver
    una diccionario compatible de ese dia con ese personal.

    Por cada dia que pase, se crea una ficha y en cada ficha obtiene el personal mas reciente y añade la version mas
    actualizada, para evitar problemas de compatabilidad y prevenir errores inesperados
    '''

    def __init__(self) -> dict:
        
        '''version -> v1, v2, v3 of services'''
        self.response = {}
        services_raw = configure.find_one({ "_id": ObjectId("65ec5f9f88701955b30661a5") })
        


        #print('services_raw ->', services_raw)
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

                self.response = {
                    "info": "Conversión de los servicios éxitosa",
                    "status": "ok",
                    "type": "SUCCESS",
                    "data": dict_services
                }
            else:
                if not verify_hour:
                    self.response = {
                        "info": "Las horas no cumplen con la condición, deben ser mayor a 0 y menor/igual a 4",
                        "status": "no",
                        "type": "VERIFY_HOUR_ERROR"
                    }
                    break

                if not verify_minutes:
                    self.response = {
                        "info": "Los minutos no son validos, no cumplen con la condicion de 0/30 minutos",
                        "status": "no",
                        "type": "VERIFY_MINUTES_ERROR"
                    }
                    break
        
        #print('dict_services ->', dict_services)
        #pprint(dict_services)