import unittest
import requests

class TestAPI(unittest.TestCase):
    def setUp(self):
        # Configurar el cliente HTTP para enviar solicitudes a la API local
        self.base_url = "http://localhost:8000/app/api/v1"

    def test_get_users(self):
        # Probar la ruta para obtener todos los usuarios
        response = requests.get(f"{self.base_url}/admin/items/10")
        self.assertEqual(response.status_code, 200)
        # Verificar la estructura de la respuesta JSON
        #self.assertIn("users", response.json())

    '''
    def test_create_user(self):
        # Probar la creación de un nuevo usuario
        new_user_data = {"username": "testuser", "email": "test@example.com"}
        response = requests.post(f"{self.base_url}/users", json=new_user_data)
        self.assertEqual(response.status_code, 201)
        # Verificar que el usuario fue creado correctamente
        self.assertIn("id", response.json())
    '''

if __name__ == "__main__":
    unittest.main()
