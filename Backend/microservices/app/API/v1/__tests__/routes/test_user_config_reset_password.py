import pytest
import httpx
from termcolor import cprint
from Backend.microservices.app.API.v1.__tests__.routes.config import BASE_URL, login_credentials
from Backend.microservices.app.API.v1.logging_config import logger

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_user_config_reset_password():
    #email: str = "exampleandrian@gmail.com"
    #password: str = "fuck_you"
    
    data_login: dict = login_credentials
    #print(BASE_URL)

    try:
        # Desactiva la verificación de certificados SSL en httpx
        with httpx.Client() as client:
            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/public/login",
                json=data_login
            )

            logger.info(f"USER CONFIG: {response.json()}")

            # Verifica el código de estado HTTP
            assert response.status_code == 200

            # Obtén el contenido de la respuesta
            response_json: dict = response.json()

            # Imprime el contenido de la respuesta
            cprint(f"\nResponse: {response_json}\n", "green", "on_black")

            response_json["current_psw"] = data_login["password"]
            response_json["new_psw"] = data_login["password"]

            logger.info(f"USER CONFIG: {response_json}")

            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/restricted/user/config/reset_password",
                json=response_json
            )

            logger.info(f"USER CONFIG: {response.json()}")

            # Verifica el código de estado HTTP
            assert response.status_code == 200

            print(response.json())

    except httpx.RequestError as e:
        # Manejo de excepciones de la librería httpx
        print(f"Request failed: {e}")