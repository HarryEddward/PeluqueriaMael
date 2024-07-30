import httpx

from Backend.microservices.conversor.config.config import Config


config: dict = Config()
host: str = config['host']
app: str = config['app']

port: str = app['CryptoAPI']['net']['port']
ssl: str = app['CryptoAPI']['ssl']
protcol: str = 'https' if ssl else 'http'
BASE_URL: str = f"{protcol}://{host}:{port}"

def encrypt(text: str) -> str:

    """
    _summary_
    """
    with httpx.Client() as client:

        to_encrypt: bytes = text.encode("utf-8")
        result: dict = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/encrypt", content=to_encrypt, headers={"Content-Type": "application/octet-stream"})
        content: bytes = result.content

        if content != b'0' or result.status != 200:
            raise Exception("Hubo un error a la hora de encriptar o decriptar")

        return result.content

def decrypt(encrypted_text: str) -> str:
        

    with httpx.Client() as client:
        to_encrypt: bytes = encrypted_text.encode("utf-8")
        result: dict = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/encrypt", content=to_encrypt, headers={"Content-Type": "application/octet-stream"})
        content: bytes = result.content

        if content != b'0' or result.status != 200:
            raise Exception("Hubo un error a la hora de encriptar o decriptar")

        return result.content

