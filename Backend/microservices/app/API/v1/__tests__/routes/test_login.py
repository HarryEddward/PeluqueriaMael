import httpx
from termcolor import cprint
from Backend.microservices.app.API.v1.__tests__.routes.config import BASE_URL

def test_encrypt_gpu():
    with httpx.Client() as client:

        email: str = "exampleandrian@gmail.com"
        password: str = "fuck_you"


        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/encrypt", content=text_to_encrypt, headers={"Content-Type": "application/octet-stream"})

        assert response.status_code == 200
        encrypted_content = response.content

        cprint(f"\Response: {encrypted_content}\n", "green", "on_black")

