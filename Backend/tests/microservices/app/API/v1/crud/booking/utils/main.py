import unittest
from Backend.microservices.app.API.v1.crud.booking.utils.serviceToPersonal import serviceToPersonal

from pydantic import BaseModel

from pydantic_extra_types.phone_numbers import PhoneNumber

class TestBookingUtilsCRUD(unittest.TestCase):
    
    def setUp(self) -> None:
        pass

    
    #@unittest.skip("#")
    def test_serviceToPersonal(self) -> None:
        
        personal = serviceToPersonal(
            serviceToPersonal.service(service="peinar_con_secador")
        )
        print(personal.response)
        self.assertEqual(personal.response["status"], "ok")


if __name__ == '__main__':
    unittest.main()