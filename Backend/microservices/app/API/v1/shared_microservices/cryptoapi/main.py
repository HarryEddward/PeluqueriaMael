import httpx
from pydantic import BaseModel, ValidationError, field_validator
from validate_utf8 import find_utf8_errors
import re
from typing import Union
from Backend.microservices.conversor.config.config import Config
from Backend.microservices.app.API.v1.logging_config import logger

# Configuración
config: dict = Config()
app: str = config['app']

host: str = app['CryptoAPI']['host']
port: str = app['CryptoAPI']['net']['port']
ssl: str = app['CryptoAPI']['ssl']
protocol: str = 'https' if ssl else 'http'
BASE_URL: str = f"{protocol}://{host}:{port}"

# Expresiones regulares para validación
patron_binario = re.compile(b'^[\x20-\x7E]+$')  # Permite solo caracteres imprimibles ASCII
patron_texto = re.compile(r'^[a-zA-Z0-9\s.,!?@\'"_-]+$')  # Permite solo caracteres permitidos

class DecryptBytes(BaseModel):
    encrypted: bytes


class EncryptText(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def check_valid_utf8(cls, value: str) -> Union[str, ValueError]:
        # Verificar UTF-8
        errors = find_utf8_errors(value.encode('utf-8'))
        if errors:
            raise ValueError(f'El texto contiene caracteres que no están codificados en UTF-8: {errors}')
        
        # Convertir a bytes para validar caracteres permitidos
        texto_bytes = value.encode('utf-8')
        if not patron_binario.fullmatch(texto_bytes):
            raise ValueError('El texto contiene caracteres no imprimibles en ASCII.')

        """ # Verificar caracteres permitidos en texto
        if not patron_texto.fullmatch(value):
            logger.info(f"VALUE ERROR: {value}")
            raise ValueError('El texto contiene caracteres especiales no permitidos.')
        """
        return value

def encrypt(text: str) -> Union[str, Exception, ValueError]:
    """Encriptar texto usando una API.

    Args:
        text (str): El texto a encriptar.

    Raises:
        Exception: Si ocurre un error durante la encriptación.

    Returns:
        bytes: Texto encriptado.
    """
    try:
        valid_text = EncryptText(text=text)
    except ValidationError as e:
        raise ValueError(f"Error de validación: {e}")
    
    with httpx.Client() as client:
        to_encrypt: bytes = valid_text.text.encode("utf-8")
        print(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/encrypt")
        result = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/encrypt", content=to_encrypt, headers={"Content-Type": "application/octet-stream"})
        content: bytes = result.content
        #print(content, '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')

        if content == b'0' or result.status_code != 200:
            raise Exception("Hubo un error a la hora de encriptar")
        
        if not result.content.decode("ascii"):
            raise ValueError("Los bytes no son formateados con letras ascii")

        return (result.content).decode()

def decrypt(encrypted: str) -> Union[str, Exception]:
    """Desencriptar texto usando una API.

    Args:
        encrypted (bytes): Texto encriptado.

    Raises:
        Exception: Si ocurre un error durante la desencriptación.

    Returns:
        bytes: Texto desencriptado.
    """

    encrypted: bytes = encrypted.encode()
    with httpx.Client() as client:
        result = client.post(f"{BASE_URL}/cryptoapi/app/api/v1/gpu/decrypt", content=encrypted, headers={"Content-Type": "application/octet-stream"})
        content: bytes = result.content

        if content == b'0' or result.status_code != 200:
            raise Exception("Hubo un error a la hora de encriptar o desencriptar")

        return content.decode()

if __name__ == "__main__":
    import time

    text = "sadsadsadsasa"  # Usa una cadena válida para probar
    start_time = time.time()

    for i in range(1000):
        encrypted_text = encrypt(text + str(i))
        #print(f'Encrypted text: {encrypted_text}')

        decrypted_text = decrypt(encrypted_text)
        #print(f'Decrypted text: {decrypted_text.decode("utf-8")}')

    end_time = time.time()
    print(f'Execution time: {end_time - start_time}')
