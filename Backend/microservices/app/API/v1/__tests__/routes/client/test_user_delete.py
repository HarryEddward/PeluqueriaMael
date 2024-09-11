import pytest
import httpx
from termcolor import cprint
from Backend.microservices.app.API.v1.__tests__.routes.config import BASE_URL, delete_credentials
from Backend.microservices.app.API.v1.logging_config import logger

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_user_delete():
    #email: str = "adriansupalumbedsadsarasddsadgssdaasasadsadsdmarkzukrb191010@gmail.com"
    #password: str = "fuck_yo"
    
    data: dict = delete_credentials
    try:
        with httpx.Client() as client:
            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/public/register",
                json=data
            )
            
            logger.info(f"REGISTER DELTE USER: {response.json()}")

            # Verifica el código de estado HTTP
            assert response.status_code == 200

            # Obtén el contenido de la respuesta en formato JSON
            response_json: dict = response.json()

            # Verifica que el JSON contenga las claves 'token_id' y 'token_data'
            assert "token_id" in response_json, "'token_id' not found in response"
            assert "token_data" in response_json, "'token_data' not found in response"

            # Imprime el contenido de la respuesta (puedes comentar esto si no es necesario)
            cprint(f"\nResponse JSON: {response_json}\n", "green", "on_black")
            
            response_json["verify"] = True
            logger.info(response_json)

            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/restricted/user/delete",
                json=response_json
            )

            logger.info(f"USER DELETE: {response.json()}, {response.status_code}")

            print(response.content)

    except httpx.RequestError as e:
        # Manejo de excepciones de la librería httpx
        print(f"Request failed: {e}")

