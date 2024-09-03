import pytest
import httpx
from termcolor import cprint
from Backend.microservices.app.API.v1.__tests__.routes.config import BASE_URL, login_credentials
from Backend.microservices.app.API.v1.logging_config import logger

class Config:
    id_appointment: str = ""

    @classmethod
    def set_id_appointment(cls, appointment_id: str):
        cls.id_appointment = appointment_id

    @classmethod
    def get_id_appointment(cls) -> str:
        return cls.id_appointment

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
@pytest.mark.order(1)
def test_booking_add():
    data: dict = login_credentials

    try:
        with httpx.Client() as client:
            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/public/login",
                json=data
            )
            #print(response)

            assert response.status_code == 200

            response_json: dict = response.json()

            cprint(f"\nResponse: {response_json}\n", "green", "on_black")
            
            data_appointment: dict = {
                "token_id": response_json["token_id"],
                "token_data": response_json["token_data"],
                "day_date": 21,
                "month_date": 9,
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

            logger.info(f"ADD APPONITMENT: {response.json()}")

            response_json = response.json()
            print(response_json)

            # Guardar el id_appointment en Config
            Config.set_id_appointment(response_json["data"]["id_appointment"])

    except httpx.RequestError as e:
        print(f"Request failed: {e}")

#@pytest.mark.skip(reason="Esta prueba está deshabilitada temporalmente.")
@pytest.mark.order(2)
def test_booking_remove():
    data: dict = login_credentials
    print(BASE_URL)

    try:
        with httpx.Client() as client:

            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/public/login",
                json=data
            )
            print(response)

            assert response.status_code == 200

            response_json: dict = response.json()

            cprint(f"\nResponse: {response_json}\n", "green", "on_black")

            # Usar el id_appointment guardado en Config
            id_appointment = Config.get_id_appointment()
            
            data_appointment: dict = {
                "token_id": response_json["token_id"],
                "token_data": response_json["token_data"],
                "id_reserva": Config.get_id_appointment()
            }

            print(data_appointment)

            response: httpx.Response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/restricted/booking/remove",
                json=data_appointment
            )

            logger.info(f"REMOVE APPONITMENT: {response.json()}")

            print(response.json())

    except httpx.RequestError as e:
        print(f"Request failed: {e}")
