import unittest
from Backend.microservices.app.API.v1.crud.booking.add import AddBooking
from Backend.microservices.app.API.v1.crud.booking.utils.conversorServices import conversorServices
from Backend.microservices.app.API.v1.crud.booking.utils.serviceToPersonal import serviceToPersonal
from Backend.microservices.app.API.v1.crud.booking.utils.workerLessBusy import workerLessBusy
from Backend.microservices.app.API.v1.db.database import configure, reservas

from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber
from bson import ObjectId
from datetime import datetime

class TestUsersBookingCRUD(unittest.TestCase):
    
    def setUp(self) -> None:
        pass

    
    #@unittest.skip("#")
    def test_Add(self) -> None:
        name_service = "peinar_con_secador"

        day = datetime(2024, 3, 26)
        appointment = reservas.find_one({"fecha": {"$eq": day}})
        personal_raw = configure.find_one({ "_id": ObjectId("661f915fac2b216927f37257") })

        personal = serviceToPersonal(
            serviceToPersonal.service(service=name_service)
        )

        if personal.response["status"] == 'no':
            print(personal.response, 401)
            return personal.response

        specific_personal = personal_raw["personal"][personal.response["data"]]

        '''
        Busca el trabajador de el día de los trabajadores, todo los trabajadores

        Vincular una referencia de diferentes versiones de trabajadores por cada cambio que se
        haga, para evitar difernetes cambios incompatibles entre nuevos trabajadores que se añadan
        por cada lista diaria de las reservas a hacer.

        Evitar incompatibilidades
        '''
        worker_less_bussy = workerLessBusy(
            workerLessBusy.structure(
                rama_profesionales=specific_personal,
                professionals=appointment
            )
        )
        if not worker_less_bussy.response["status"] == 'ok':
            print(worker_less_bussy.response, 401)
            return worker_less_bussy.response
        
        print('worker less bussy->', worker_less_bussy.response["data"])

        services = conversorServices()

        if not services.response["status"] == 'ok':
            print(services.response, 401)
            return services.response

        print(services.response["data"])
        services = services.response["data"]   
        
        booking = AddBooking(
            AddBooking.structure(
                day=26,
                month=3,
                year=2024,
                professional=worker_less_bussy.response["data"],
                period="afternoon",
                start_time="17:00",
                service_duration=services[name_service][0],
                person_id="65ec610288701955b30661a8",
                service=name_service
            )
        )
        print('here')
        print('\n\nresponse addbooking ->', booking.response)
        print('here')
        self.assertEqual(booking.response["status"], 'ok')

    @unittest.skip("#")
    def test_Remove(self) -> None:

        
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()