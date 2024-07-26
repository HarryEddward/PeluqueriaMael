import unittest
from Backend.microservices.app.API.v1.crud.users.add import AddUser
from Backend.microservices.app.API.v1.crud.users.find import FindUser, FindSecretJWTID
from Backend.microservices.app.API.v1.crud.users.update import UpdateUser
from Backend.microservices.app.API.v1.crud.users.validation import ValidationUser

from pydantic import BaseModel

from pydantic_extra_types.phone_numbers import PhoneNumber


class TestUsersCRUD(unittest.TestCase):
    
    def setUp(self) -> None:
        pass

    @unittest.skip("#")
    def test_Find(self) -> None:

        #->
        Find_user = FindUser({"email": "he070070@gmail.com"})
        

        user = FindUser.secret_jwt(FindSecretJWTID(id="661a4d120b025320742dfe09"))

        
        #->
        print('1->', user.response)
        self.assertEqual(user.response["status"], "ok")

        #print(find_user.response)
        #self.assertEqual(find_user.response["status"], "ok")


    @unittest.skip("#")
    def test_Add(self) -> None:
        
        #->
        add_user = AddUser({
            "email": "adrianelcapo@gmail.com",
            "password": "adrianelcapo"        
        })
        #->
        
        print(add_user.response)
        self.assertEqual(add_user.response["status"], "ok")
    

    @unittest.skip("#")
    def test_Update(self) -> None:
        
        #-> PASSWORD
        renew_psw = UpdateUser.password({
            "email": "adrianelcapo@gmail.com",
            "password": "adrianelcapo",
            "new_password": "fuck_you"
        })
        #->
        
        print('res, update, psw: ', renew_psw.response)
        self.assertEqual(renew_psw.response["status"], "ok")


        #->
        renew_secret = UpdateUser.secret_jwt({
            "email": "adrianelcapo@gmail.com",
            "password": "fuck_you",
        })
        #->

        
        print('res, update, secret: ', renew_secret.response)
        self.assertEqual(renew_secret.response["status"], "ok")


        
    #@unittest.skip("#")
    def test_Validate(self) -> None:

        #->
        user = ValidationUser({
            "email": "adrianelcapo@gmail.com",
            "password": "fuck_you",
            "info": False
        })
        #->

        print(user.response)
        self.assertEqual(user.response["status"], "ok")

    
if __name__ == '__main__':
    unittest.main()