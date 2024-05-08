import requests
import json
import unittest

class TestSaveTokensToJson(unittest.TestCase):
    def setUp(self):
        self.url = "https://localhost:8000/app/api/v1/client/restricted/booking"

    @unittest.skip("Falta añadir la validación de pydantic en la ruta y hacer uso de la ruta por parametros")
    def test_path_add(self) -> None:

        '''
        
        '''
        with open('./data.json', 'r') as archivo:
            data = json.load(archivo)
        
        token_id = data["token_id"]
        token_data = data["token_data"]

        send = {
            "token_id": token_id,
            "token_data": token_data,
            "day_date": 7,
            "month_date": 4,
            "year_date": 2024,
            "name_service": "montaje_de_mechas"
        }

        response = requests.post(self.url + "/add", json=send, verify=False)

        #print("Código de estado de la respuesta:", response.status_code)
        print(response)

        raw_data = response.json()
        print('\n', raw_data, '\n')

        #El token si aunque reciba un fallo se debe de refrescar cada vez que hace una operacion, obligatoriamente
        data["token_data"] = raw_data["renew"]["token"]

        with open('./data.json', 'w') as archivo:
            json.dump(data, archivo)

        #print(token_id, token_data)
        self.assertEqual(response.status_code, 200)

    
    #@unittest.skip("")
    def test_path_remove(self):
        with open('data.json', 'r') as archivo:
            data = json.load(archivo)
        
        token_id = data["token_id"]
        token_data = data["token_data"]

        send = {
            "token_id": token_id,
            "token_data": token_data,
            "id_reserva": "5bb574f9-da23-425f-b12a-ce543e3c8766"
        }

        response = requests.post(self.url + "/remove", json=send, verify=False)

        #print("Código de estado de la respuesta:", response.status_code)
        print(response)

        raw_data = response.json()
        print('\n', raw_data, '\n')

        #El token si aunque reciba un fallo se debe de refrescar cada vez que hace una operacion, obligatoriamente
        data["token_data"] = raw_data["renew"]["token"]

        with open('data.json', 'w') as archivo:
            json.dump(data, archivo)

        #print(token_id, token_data)
        self.assertEqual(response.status_code, 200)

        

if __name__ == '__main__':
    unittest.main()