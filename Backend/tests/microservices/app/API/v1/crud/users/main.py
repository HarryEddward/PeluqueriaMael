import unittest
from Backend.microservices.app.API.v1.crud.users.add import AddUser
from Backend.microservices.app.API.v1.crud.users.find import FindUser
from Backend.microservices.app.API.v1.crud.users.update import UpdateUser
from Backend.microservices.app.API.v1.crud.users.validation import ValidationUser


from pydantic_extra_types.phone_numbers import PhoneNumber


class TestUsersCRUD(unittest.TestCase):
    
    def setUp(self) -> None:
        pass

    @unittest.skip("#")
    def test_Find(self) -> None:

        #->
        find_user = FindUser({"email": "he070070@gmail.com"})
        #->

        print(find_user.response)
        self.assertEqual(find_user.response["status"], "ok")


    @unittest.skip("Evitar crear usuarios en exceso")
    def test_Add(self) -> None:
        
        #->
        add_user = AddUser({
            "email": "adrianelcapo@gmail.com",
            "number_phone": PhoneNumber("+34643567016"),
            "password": "adrianelcapo"        
        })
        #->
        
        print(add_user.response)
        self.assertEqual(add_user.response["status"], "ok")
    

    #@unittest.skip("Evitar cambiar de contraseña repetidamente")
    def test_Update(self) -> None:
        
        ''' #-> PASSWORD
        renew_psw = UpdateUser.password({
            "email": "adrianelcapo@gmail.com",
            "password": "adrianelcapo",
            "new_password": "fuck_you"
        })
        #->'''
        #print('res, update, psw: ', renew_psw.response)
        #self.assertEqual(renew_psw.response["status"], "ok")

        #->
        renew_secret = UpdateUser.secret_jwt({
            "email": "adrianelcapo@gmail.com",
            "password": "fuck_you",
        })
        #->

        
        print('res, update, secret: ', renew_secret.response)
        self.assertEqual(renew_secret.response["status"], "ok")


        
    @unittest.skip("Dejar de validar")
    def test_Validate(self) -> None:

        #->
        user = ValidationUser({
            "email": "adrianelcapo@gmail.com",
            "password": "fuck_you"
        })
        #->

        print(user.response)
        self.assertEqual(user.response["status"], "ok")

    
if __name__ == '__main__':
    unittest.main()