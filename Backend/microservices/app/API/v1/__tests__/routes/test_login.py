import httpx
from termcolor import cprint
from Backend.microservices.app.API.v1.__tests__.routes.config import BASE_URL

def test_login():
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
            response = client.post(
                f"{BASE_URL}/api/app/api/v1/client/public/login",
                json=data
            )
            print(response)

            # Verifica el código de estado HTTP
            assert response.status_code == 200

            # Obtén el contenido de la respuesta
            encrypted_content = response.content

            # Imprime el contenido de la respuesta
            cprint(f"\nResponse: {encrypted_content}\n", "green", "on_black")

    except httpx.RequestError as e:
        # Manejo de excepciones de la librería httpx
        print(f"Request failed: {e}")
