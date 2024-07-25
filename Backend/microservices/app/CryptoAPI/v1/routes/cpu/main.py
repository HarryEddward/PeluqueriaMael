from fastapi import (
    APIRouter,
    Request,
    Response
)
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from Backend.microservices.app.CryptoAPI.v1.config import env
from Backend.microservices.app.CryptoAPI.v1.routes.cpu.responses import (
     responses_encrypt
    ,responses_decrypt
)

import os
import numpy as np

'''
Se cargaran las variables de .env en modo producción
'''
'''

cryptography_key = os.getenv('CRYPTO_KEY')
cryptography_key = cryptography_key.encode()

# Genera una clave de cifrado. En una aplicación real, guarda esta clave en un lugar seguro.
cipher_suite = Fernet(cryptography_key)
'''


class CryptoManager:
    __instance = None

    @staticmethod
    def get_instance() -> None:
        if CryptoManager.__instance is None:
            # Aquí puedes cargar la clave desde tu entorno o configuración
            if env == "dev":
                env_path = find_dotenv()
                load_dotenv(dotenv_path=env_path)

            cryptography_key = os.getenv('KEY_CRYPTO_CPU')
            print(cryptography_key)
            if cryptography_key:
                cryptography_key = cryptography_key.encode()
            else:
                raise ValueError("No se encontró la clave de cifrado en el entorno.")
            
            
            CryptoManager.__instance = Fernet(cryptography_key)
        
        return CryptoManager.__instance
    
crypto_manager = CryptoManager.get_instance()

router = APIRouter()

@router.post('/encrypt', responses=responses_encrypt)
async def Encrypt_(request: Request):
    
    """
    Encripta información por bytes a través por el content-type: application/octet-stream

    Args:
        data (str): Texto a encriptar
    
    Return:
        bytes: Recibe el texto encritpado sin procesar a texto, esta a bytes
    """
    
    # Acceder al texto decodificado desde el middleware
    bytes_ = request.state.body

    # Validar que el contenido no esté vacío
    if len(bytes_) == 0 or bytes_.isspace():
        return Response(content=b'0', media_type='application/octet-stream')

    # Procesar el texto
    try:
        resultado = crypto_manager.encrypt(bytes_)
        
    except Exception:
        return Response(content=b'0', media_type='application/octet-stream')

    return Response(content=resultado, media_type='application/octet-stream')


@router.post('/decrypt', responses=responses_decrypt)
async def Decrypt_(request: Request):
    
    """
    Decripta información por bytes a través por el content-type: application/octet-stream

    Args:
        data (str): Texto a decriptar
    
    Return:
        bytes: Recibe el texto decritpado sin procesar a texto, esta a bytes
    """
    
    
    # Acceder al texto decodificado desde el middleware
    bytes_ = request.state.body

    # Validar que el contenido no esté vacío
    if len(bytes_) == 0 or bytes_.isspace():
        del bytes_
        return Response(content=b'0', media_type='application/octet-stream')

    try:
        # Procesar el texto
        resultado = crypto_manager.decrypt(bytes_)
        
    except Exception as e:
        # No se elimina de forma explicita la vairbale resultado, porque si hay un error, no se podra borrar por el error, y generara otro error
        del bytes_
        return Response(content=b'0', media_type='application/octet-stream')

    return Response(content=resultado, media_type='application/octet-stream')