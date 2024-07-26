import unittest
#from Backend.microservices.app.API.v1.crud.users.booking.add import AddBookingUser, AddAppointment
from Backend.microservices.app.API.v1.crud.users.booking.remove import RemoveBookingUser

from pydantic import BaseModel

from pydantic_extra_types.phone_numbers import PhoneNumber


class TestUsersBookingCRUD(unittest.TestCase):
    
    def setUp(self) -> None:
        pass

    
    @unittest.skip("#")
    def test_Add(self) -> None:
        
        AddBookingUser(
            AddAppointment(
                responsable_appointment="",
                id_appointment="",
                period="",
                start_time="",
                person_id="",
                service=""
            )
        )
        self.assertEqual(True, True)

    #@unittest.skip("#")
    def test_Remove(self) -> None:


        remove_booking = RemoveBookingUser(
            RemoveBookingUser.structure(
                id_appointment="05b7f6ae-d75c-43bb-97f3-67c8044c81e0",
                person_id="65ec610288701955b30661a8"
            )
        )
        print(remove_booking.response)
        self.assertEqual(remove_booking.response["status"], "ok")

if __name__ == '__main__':
    unittest.main()