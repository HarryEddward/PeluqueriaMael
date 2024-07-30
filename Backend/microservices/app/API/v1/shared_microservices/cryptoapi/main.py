import httpx

from Backend.microservices.conversor.config.config import Config

"""
A la hora de hacer úso encriptar y decriptar texto hay que tener estas consideraciónes:

La codificación y la decodificación se hace mediante utf-8, la forma de encriptar y decriptar
no esta preparada para usarse con accentos como hace latin-1-
"""

config: dict = Config()
host: str = config['host']
app: str = config['app']

port: str = app['CryptoAPI']['net']['port']
ssl: str = app['CryptoAPI']['ssl']
protcol: str = 'https' if ssl else 'http'
BASE_URL: str = f"{protcol}://{host}:{port}"

def encrypt(text: str) -> bytes:

    """AI is creating summary for 

    Raises:
        Exception: [description]

    Returns:
        [type]: [description]
    """
    with httpx.Client() as client:

        to_encrypt: bytes = text.encode("utf-8")
        result = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/encrypt", content=to_encrypt, headers={"Content-Type": "application/octet-stream"})
        content: bytes = result.content

        #print(content)

        if content == b'0' or result.status_code != 200:
            #print(content != b'0')
            #print(result.status_code != 200)
            raise Exception("Hubo un error a la hora de encriptar")

        return result.content

def decrypt(encrypted: bytes) -> bytes:
    """AI is creating summary for decrypt

    Args:
        encrypted_text (str): [description]

    Raises:
        Exception: [description]

    Returns:
        str: [description]
    """

    with httpx.Client() as client:
        print(encrypted)
        #to_decrypt: bytes = encrypted_text.encode("utf-8")
        result = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/decrypt", content=encrypted, headers={"Content-Type": "application/octet-stream"})
        content: bytes = result.content

        if content == b'0' or result.status_code != 200:
            print(content)
            raise Exception("Hubo un error a la hora de encriptar o decriptar")

        return result.content


if __name__ == "__main__":

    text: str = "hola que tal tu día?"
    encrypt_text: str = encrypt(text)
    
    print(encrypt_text)

    print(decrypt(encrypt_text))