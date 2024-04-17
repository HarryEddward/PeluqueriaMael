import unittest
from Backend.microservices.app.API.v1.services.auth import JWToken  # Importa JWToken desde el módulo auth


from pydantic_extra_types.phone_numbers import PhoneNumber


class TestAuthJWT(unittest.TestCase):
    
    def setUp(self) -> None:
        pass
    #@unittest.skip("#")
    def test_JWT_create(self) -> None:

        secret: str = "kDchltdpfcpFSomA_T)1zP8XoPPiXUp1yz4Afczn(%JeoEUco+5U)MBcqeb97W(_jA^!yQXKjGYCY&kD#LqgoJSJ)e)nMi9lud6Wqff!hR@(uk=D3olXRPh6"
        #->
        self.create_jwt = JWToken.create({
            "email": "adrianelcapo@gmail.com",
            "password": "fuck_you"
        }, secret)
        #->

        print(self.create_jwt)
        self.assertEqual(self.create_jwt["status"], "ok")

    #@unittest.skip("#")
    def test_JWT_check(self) -> None:
        
        
        secret = "kDchltdpfcpFSomA_T)1zP8XoPPiXUp1yz4Afczn(%JeoEUco+5U)MBcqeb97W(_jA^!yQXKjGYCY&kD#LqgoJSJ)e)nMi9lud6Wqff!hR@(uk=D3olXRPh6"
        
        #->
        self.check_jwt = JWToken.check("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjp7ImVtYWlsIjoiYWRyaWFuZWxjYXBvQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiZnVja195b3UifSwiZXhwIjoxNzE1NjI5MDY4fQ.Rm_XaqodTz-MsibE_SzAjZN6zyhMDjmBD1rVbxtWj9g", secret)
        #->
    
        print('Decoded ->', self.check_jwt)
        self.assertEqual(self.check_jwt["status"], "ok")
    


if __name__ == '__main__':
    unittest.main()