import pytest
import httpx
from termcolor import cprint
from Backend.microservices.app.API.v1.__tests__.routes.config import BASE_URL


#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
@pytest.mark.order(1)
def test_booking_add():
    email: str = "exampleandrian@gmail.com"
    password: str = "fuck_you"
    
    data: dict = {
        "email": email,
        "password": password
    }
    print(BASE_URL)

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

            # Imprime el contenido de la respuesta
            cprint(f"\nResponse: {response_json}\n", "green", "on_black")
            
            data_appointment: dict = {
                "token_id": response_json["token_id"],
                "token_data": response_json["token_data"],
                "day_date": 8,
                "month_date": 4,
                "year_date": 2024,
                "hour": "9:30",
                "period": "morning",
                "name_service": "peinar_con_secador"
            }

            print(data_appointment)

            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/restricted/booking/add",
                json=data_appointment
            )

            print(response.json())


    except httpx.RequestError as e:
        # Manejo de excepciones de la librería httpx
        print(f"Request failed: {e}")


@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
@pytest.mark.order(2)
def test_booking_remove():
    email: str = "exampleandrian@gmail.com"
    password: str = "fuck_you"
    
    data: dict = {
        "email": email,
        "password": password
    }
    print(BASE_URL)

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

            # Imprime el contenido de la respuesta
            cprint(f"\nResponse: {response_json}\n", "green", "on_black")
            
            data_appointment: dict = {
                "token_id": response_json["token_id"],
                "token_data": response_json["token_data"],
                "id_reserva": "2ac5f028-4419-427e-bf49-4e855967952b"
            }

            print(data_appointment)

            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/restricted/booking/remove",
                json=data_appointment
            )

            print(response.json())


    except httpx.RequestError as e:
        # Manejo de excepciones de la librería httpx
        print(f"Request failed: {e}")