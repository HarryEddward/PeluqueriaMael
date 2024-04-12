import unittest
from microservices.app.API.v1.crud.users.add import AddUser
from microservices.app.API.v1.crud.users.find import FindUser

from pydantic_extra_types.phone_numbers import PhoneNumber


class TestUsersCRUD(unittest.TestCase):
    
    def setUp(self) -> None:
        pass

    def test_Find(self) -> None:

        #->
        find_user = FindUser({"email": "he070070@gmail.com"})
        #->

        print(find_user.response)
        self.assertEqual(find_user.response["status"], "ok")

    def test_Add(self) -> None:
        
        #->
        add_user = AddUser({
            "email": "he07880070@gmail.com",
            "number_phone": PhoneNumber("+34643567016"),
            "password": "password"        
        })
        #->
        
        print(add_user.response)
        self.assertEqual(add_user.response["status"], "ok")
    
if __name__ == '__main__':
    unittest.main()