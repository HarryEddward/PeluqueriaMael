import unittest
from Backend.microservices.app.API.v1.crud.booking.utils.serviceToPersonal import serviceToPersonal
from Backend.microservices.app.API.v1.crud.booking.utils.workerLessBusy import workerLessBusy
from Backend.microservices.app.API.v1.crud.booking.utils.conversorServices import conversorServices

from Backend.microservices.app.API.v1.db.database import reservas
from Backend.microservices.app.API.v1.db.database import configure
from datetime import datetime
from bson import ObjectId

from pydantic import BaseModel

from pydantic_extra_types.phone_numbers import PhoneNumber

class TestBookingUtilsCRUD(unittest.TestCase):
    
    def setUp(self) -> None:
        try:
            day = datetime(2024, 3, 26)
            self.appointment = reservas.find_one({"fecha": {"$eq": day}})
            self.personal_raw = configure.find_one({ "_id": ObjectId("661f915fac2b216927f37257") })
            
            # Llama a test_serviceToPersonal y almacena el resultado en una variable
            self.personal = self.test_serviceToPersonal()
            
            # Llama a test_workerLessBusy y pasa el resultado de test_serviceToPersonal como argumento
            self.test_workerLessBusy()
        except Exception as e:
            print('Error en la DB')
    

    #@unittest.skip("#")
    def test_serviceToPersonal(self) -> None:
        
        self.personal = serviceToPersonal(
            serviceToPersonal.service(service="peinar_con_secador")
        )
        
        #print(self.personal.response)
        self.assertEqual(self.personal.response["status"], "ok")

        return self.personal


    #@unittest.skip("#")
    def test_workerLessBusy(self) -> None:
        
        
        specific_personal = self.personal_raw["personal"][self.personal.response["data"]]

        worker_more_free = workerLessBusy(
            workerLessBusy.structure(
                rama_profesionales=specific_personal,
                professionals=self.appointment
            )
        )

        #print(worker_more_free.response)
        self.assertEqual(worker_more_free.response["status"], "ok")


    #@unittest.skip("#")
    def test_conversorServices(self) -> None:

        services = conversorServices()

        #print('\n services ->', services.response["data"])
        self.assertEqual(services.response["status"], 'ok')

if __name__ == '__main__':
    unittest.main()