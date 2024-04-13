import unittest
from Backend.microservices.app.API.v1.services.auth import JWToken  # Importa JWToken desde el módulo auth


from pydantic_extra_types.phone_numbers import PhoneNumber


class TestAuthJWT(unittest.TestCase):
    
    def setUp(self) -> None:
        pass
    @unittest.skip("#")
    def test_JWT_create(self) -> None:

        #secret: str = "+tInFHGmJ7Di41!6Exnc(qnVuJ9KsVlI5u)tE3gXHLIF1$nnUCyx)Zdb&9+HLLiC$s9vOXXnh*NauYPBIU5fcNEh#19FNbe@t$Tb%XY(qkzP&LpN#=Zj1i@M"
        #->
        self.create_jwt = JWToken.create({
            "id": "661a4d120b025320742dfe09"
        })
        #->

        print(self.create_jwt)
        self.assertEqual(self.create_jwt["status"], "ok")

    #@unittest.skip("#")
    def test_JWT_check(self) -> None:
        
        secret = "-^-Yw%Gy@nUlJ@bDz6TGNX3B%#kvY6uY$EO+LmvC(%cRN4@6#7WePYTi899i0tB3sXCY3K260KMRn1XV6o#y5@G7xYoMyFNQevD4w6gKIMfhrJ2_lUPWyg1r"
        
        #->
        self.check_jwt = JWToken.check("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbmZvIjp7ImVtYWlsIjoiYWRyaWFuZWxjYXBvQGdtYWlsLmNvbSIsInBhc3N3b3JkIjoiZnVja195b3UifSwiZXhwIjoxNzE1NjI3Nzk2fQ.fTxdy_7X63-ypQnYib42HMYQ2_Zwa3o16BvBTwsugjI", secret)
        #->
    
        print('Decoded ->', self.check_jwt)
        self.assertEqual(self.check_jwt["status"], "ok")
    


if __name__ == '__main__':
    unittest.main()