import pytest
import httpx
from Backend.microservices.conversor.config.config import Config

config: dict = Config()
host: str = config['host']
app: str = config['app']

port: str = app['CryptoAPI']['net']['port']
ssl: str = app['CryptoAPI']['ssl']
protcol: str = 'https' if ssl else 'http'


BASE_URL: str = f"{protcol}://{host}:{port}"
print(BASE_URL)

"""
   _,.----.      _ __                 
 .' .' -   \  .-`.' ,`.  .--.-. .-.-. 
/==/  ,  ,-' /==/, -   \/==/ -|/=/  | 
|==|-   |  .|==| _ .=. ||==| ,||=| -| 
|==|_   `-' \==| , '=',||==|- | =/  | 
|==|   _  , |==|-  '..' |==|,  \/ - | 
\==\.       /==|,  |    |==|-   ,   / 
 `-.`.___.-'/==/ - |    /==/ , _  .'  
            `--`---'    `--`..---'    
"""


def test_encrypt_cpu():
    with httpx.Client() as client:
        # Texto de ejemplo para encriptar
        text_to_encrypt = b"Texto de prueba"
        
        # Realiza la solicitud POST a /encrypt
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/encrypt", content=text_to_encrypt, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta tenga un status code 200
        assert response.status_code == 200
        
        # Verifica que el contenido de la respuesta no sea b'0'
        encrypted_content = response.content
        assert encrypted_content != b'0'
        print(f"Encrypted content: {encrypted_content}")

def test_decrypt_cpu():
    with httpx.Client() as client:
        # Texto de ejemplo para encriptar y luego desencriptar
        text_to_encrypt = b"Texto de prueba"
        
        # Primero, encripta el texto
        encrypt_response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/encrypt", content=text_to_encrypt, headers={"Content-Type": "application/octet-stream"})
        encrypted_content = encrypt_response.content
        
        # Asegúrate de que el texto fue encriptado correctamente
        assert encrypt_response.status_code == 200
        assert encrypted_content != b'0'
        
        # Ahora, desencripta el texto encriptado
        decrypt_response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/decrypt", content=encrypted_content, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta tenga un status code 200
        assert decrypt_response.status_code == 200
        
        # Verifica que el contenido desencriptado coincida con el texto original
        decrypted_content = decrypt_response.content
        assert decrypted_content == text_to_encrypt
        print(f"Decrypted content: {decrypted_content}")

def test_encrypt_empty_data():
    with httpx.Client() as client:
        # Texto vacío
        text_to_encrypt = b""
        
        # Realiza la solicitud POST a /encrypt
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/encrypt", content=text_to_encrypt, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta sea b'0'
        assert response.content == b'0'
        print(f"Empty data encrypt response: {response.content}")

def test_decrypt_empty_data():
    with httpx.Client() as client:
        # Texto vacío
        text_to_decrypt = b""
        
        # Realiza la solicitud POST a /decrypt
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/decrypt", content=text_to_decrypt, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta sea b'0'
        assert response.content == b'0'
        print(f"Empty data decrypt response: {response.content}")

def test_decrypt_invalid_data():
    with httpx.Client() as client:
        # Datos aleatorios no encriptados
        invalid_data = b"Datos no encriptados sadsadadasd"
        
        # Realiza la solicitud POST a /decrypt
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/decrypt", content=invalid_data, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta sea b'0'
        assert response.content == b'0'
        print(f"Invalid data decrypt response: {response.content}")

def test_encrypt_large_data():
    with httpx.Client() as client:
        # Datos grandes
        large_data = b"A" * 10**6  # 1 MB de datos
        
        # Realiza la solicitud POST a /encrypt
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/encrypt", content=large_data, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta tenga un status code 200
        assert response.status_code == 200
        
        # Verifica que el contenido de la respuesta no sea b'0'
        encrypted_content = response.content
        assert encrypted_content != b'0'
        print(f"Large data encrypt response: {encrypted_content[:100]}...")

def test_decrypt_large_data():
    with httpx.Client() as client:
        # Datos grandes
        large_data = b"A" * 10**6  # 1 MB de datos
        
        # Primero, encripta los datos grandes
        encrypt_response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/encrypt", content=large_data, headers={"Content-Type": "application/octet-stream"})
        encrypted_content = encrypt_response.content
        
        # Asegúrate de que el texto fue encriptado correctamente
        assert encrypt_response.status_code == 200
        assert encrypted_content != b'0'
        
        # Ahora, desencripta los datos encriptados
        decrypt_response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/decrypt", content=encrypted_content, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta tenga un status code 200
        assert decrypt_response.status_code == 200
        
        # Verifica que el contenido desencriptado coincida con el texto original
        decrypted_content = decrypt_response.content
        assert decrypted_content == large_data
        print(f"Large data decrypt response: {decrypted_content[:100]}...")

def test_encrypt_repetitive_data():
    with httpx.Client() as client:
        # Datos repetitivos
        repetitive_data = b"ABCD" * 10**5  # 400 KB de datos repetitivos
        
        # Realiza la solicitud POST a /encrypt
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/encrypt", content=repetitive_data, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta tenga un status code 200
        assert response.status_code == 200
        
        # Verifica que el contenido de la respuesta no sea b'0'
        encrypted_content = response.content
        assert encrypted_content != b'0'
        print(f"Repetitive data encrypt response: {encrypted_content[:100]}...")

def test_decrypt_repetitive_data():
    with httpx.Client() as client:
        # Datos repetitivos
        repetitive_data = b"ABCD" * 10**5  # 400 KB de datos repetitivos
        
        # Primero, encripta los datos repetitivos
        encrypt_response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/encrypt", content=repetitive_data, headers={"Content-Type": "application/octet-stream"})
        encrypted_content = encrypt_response.content
        
        # Asegúrate de que el texto fue encriptado correctamente
        assert encrypt_response.status_code == 200
        assert encrypted_content != b'0'
        
        # Ahora, desencripta los datos encriptados
        decrypt_response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/cpu/decrypt", content=encrypted_content, headers={"Content-Type": "application/octet-stream"})
        
        # Verifica que la respuesta tenga un status code 200
        assert decrypt_response.status_code == 200
        
        # Verifica que el contenido desencriptado coincida con el texto original
        decrypted_content = decrypt_response.content
        assert decrypted_content == repetitive_data
        print(f"Repetitive data decrypt response: {decrypted_content[:100]}...")

"""
      _,---.      _ __                 
  _.='.'-,  \  .-`.' ,`.  .--.-. .-.-. 
 /==.'-     / /==/, -   \/==/ -|/=/  | 
/==/ -   .-' |==| _ .=. ||==| ,||=| -| 
|==|_   /_,-.|==| , '=',||==|- | =/  | 
|==|  , \_.' )==|-  '..' |==|,  \/ - | 
\==\-  ,    (|==|,  |    |==|-   ,   / 
 /==/ _  ,  //==/ - |    /==/ , _  .'  
 `--`------' `--`---'    `--`..---'    
"""

from termcolor import cprint

def test_encrypt_gpu():
    with httpx.Client() as client:

        text_to_encrypt: bytes = b'TextToEncrypt'
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/encrypt", content=text_to_encrypt, headers={"Content-Type": "application/octet-stream"})

        assert response.status_code == 200
        encrypted_content = response.content

        assert  encrypted_content != b'0'

        cprint(f"\nEncrypted content: {encrypted_content}\n", "green", "on_black")


def test_decrypt_gpu():
    with httpx.Client() as client:

        text_to_encrypt: bytes = b'TextToEncrypt'
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/encrypt", content=text_to_encrypt, headers={"Content-Type": "application/octet-stream"})

        assert response.status_code == 200
        encrypted_content = response.content

        assert  encrypted_content != b'0'

        cprint(f"\nEncrypted content: {encrypted_content}\n", "green", "on_black")


        print(encrypted_content)
        response = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/decrypt", content=encrypted_content, headers={"Content-Type": "application/octet-stream"})
        assert response.status_code == 200
        decrypted_content = response.content

        assert  decrypted_content != b'0'

        cprint(f"\nDecrypted content: {decrypted_content}\n", "green", "on_black")