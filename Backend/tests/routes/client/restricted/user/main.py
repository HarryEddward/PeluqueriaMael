import requests
import json
import unittest

class TestSaveTokensToJson(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:8000/app/api/v1/client/restricted/user"

    #@unittest.skip("")
    def test_path_delete(self) -> None:

        '''
        
        '''
        with open('./data.json', 'r') as archivo:
            data = json.load(archivo)
        
        token_id = data["token_id"]
        token_data = data["token_data"]

        send = {
            "token_id": token_id,
            "token_data": token_data,
            "verify": True
        }

        response = requests.post(self.url + "/delete", json=send, verify=False)

        #print("Código de estado de la respuesta:", response.status_code)
        print(response)

        raw_data = response.json()
        print('\n', raw_data, '\n')

        #El token si aunque reciba un fallo se debe de refrescar cada vez que hace una operacion, obligatoriamente
        data["token_data"] = raw_data["renew"]["token"]

        with open('./data/data.json', 'w') as archivo:
            json.dump(data, archivo)

        #print(token_id, token_data)
        self.assertEqual(response.status_code, 200)

    

if __name__ == '__main__':
    unittest.main()