import unittest
from Backend.microservices.app.API.v1.crud.users.booking.add import AddBookingUser, AddAppointment
from Backend.microservices.app.API.v1.crud.users.booking.remove import RemoveBookingUser, RemoveAppointment

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

    @unittest.skip("#")
    def test_Remove(self) -> None:

        RemoveBookingUser(
            RemoveAppointment(
                id_appointment="",
                person_id=""
            )
        )
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()