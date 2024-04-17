import unittest
from Backend.microservices.app.API.v1.crud.booking.add import AddBooking, Scheme 

from pydantic import BaseModel

from pydantic_extra_types.phone_numbers import PhoneNumber


class TestUsersBookingCRUD(unittest.TestCase):
    
    def setUp(self) -> None:
        pass

    
    @unittest.skip("#")
    def test_Add(self) -> None:
        

        AddBooking(
            AddBooking.structure(
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

        
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()