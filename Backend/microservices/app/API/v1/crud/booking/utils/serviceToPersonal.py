from Backend.microservices.app.API.v1.db.database import configure
from bson import ObjectId
from pydantic import BaseModel

class serviceToPersonal:

    class service(BaseModel):
        service: str

    def __init__(self, data: service) -> None:
        self.response = {}

        '''
        Se usa para obtener el personal de ese servicio, un método de verificación
        de los servicios existente contra aquellos que no tienen.

        El tipo de cada servicio se refiere al personal, que el personal hace ese
        servicio

        Example:

        serviceToPersonal(
            serviceToPersonal.service(
                service="peinar_con_secador"
            )
        )

        Response = {
                "info": "Devolucion del servicio el tipo de personal",
                "status": "ok",
                "type": "SUCCESS",
                "data": personal del servicio
            }
        '''

        service_name = data.service  # Acceder al atributo 'service' de la instancia 'data'

        try:
            raw_personal = configure.find_one({ "_id": ObjectId("661f915fac2b216927f37257") })
            raw_services = configure.find_one({ "_id": ObjectId("65ec5f9f88701955b30661a5") })
        except Exception as e:
            self.response = {
                "info": f"Error en la base de datos: {e}",
                "status": "no",
                "type": "DATABASE_ERROR"
            }
            return

        personal = raw_personal['personal']
        services = raw_services['services']

        # Buscar el servicio por nombre y obtener su tipo
        tipo_servicio = None
        for servicio in services:
            if servicio["nombre"] == service_name:
                tipo_servicio = servicio["tipo"]
                break

        if tipo_servicio is None:
            self.response = {
                "info": f"El servicio {service_name} no existe.",
                "status": "no",
                "type": "SERVICE_NOT_FOUND"
            }
        else:
            self.response = {
                "info": "Devolucion del servicio el tipo de personal",
                "status": "ok",
                "type": "SUCCESS",
                "data": tipo_servicio
            }

