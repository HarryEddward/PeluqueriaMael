import pytest
import httpx
from termcolor import cprint
from Backend.microservices.app.API.v1.__tests__.routes.config import BASE_URL, login_credentials

@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
def test_login():
    #email: str = "exampleandrian@gmail.com"
    #password: str = "fuck_you"
    
    data: dict = login_credentials
    #print(BASE_URL)

    try:
        # Desactiva la verificación de certificados SSL en httpx
        with httpx.Client() as client:
            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/public/login",
                json=data
            )
            print(response)

            # Verifica el código de estado HTTP
            assert response.status_code == 200

            # Obtén el contenido de la respuesta
            response_json: dict = response.json()

            response_json["day"] = 28
            response_json["month"] = 3
            response_json["year"] = 2024

            # Imprime el contenido de la respuesta
            cprint(f"\nResponse: {response_json}\n", "green", "on_black")


            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/restricted/data/booking_day_sheet",
                json=response_json
            )

            assert response.status_code == 200

            print(response.json())

    except httpx.RequestError as e:
        # Manejo de excepciones de la librería httpx
        print(f"Request failed: {e}")
