import unittest
from Backend.microservices.app.API.v1.services.auth import JWToken  # Importa JWToken desde el módulo auth


from pydantic_extra_types.phone_numbers import PhoneNumber


class TestAuthJWT(unittest.TestCase):
    
    def setUp(self) -> None:
        pass

    def test_JWT_create(self) -> None:

        #->
        self.create_jwt = JWToken.create({
            "email": "he0780070@gmail.com",
            "password": "9d29djdhwdhwhd09"
        })
        #->

        print(self.create_jwt)
        self.assertEqual(self.create_jwt["status"], "ok")


    def test_JWT_check(self) -> None:
        
        #->
        self.check_jwt = JWToken.check("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjp7ImVtYWlsIjoiaGUwNzgwMDcwQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiOWQyOWRqZGh3ZGh3aGQwOSJ9LCJleHAiOjE3MTM0MzU1MDR9.jsm-d73oQvmWWeUB2ono3yuKYxmHoSVeoQWq3mAH9rI")
        #->
        
        print('Decoded ->', self.check_jwt)
        self.assertEqual(self.check_jwt["status"], "ok")
    
    '''
    No recomendable hacer uso de JWToken.renew(), puede provocar problemas de
    seguridad si no se renueva por otro token, puede incluso hackearlo. Y bueno tener
    problemas 
    '''
    def test_JWT_renew(self) -> None:

        #->
            #NO USO
        #->
        pass


if __name__ == '__main__':
    unittest.main()