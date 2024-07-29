from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from dotenv import find_dotenv, load_dotenv
from Backend.microservices.app.CryptoAPI.v1.routes.gpu.responses import (
    responses_encrypt,
    responses_decrypt
)
from Backend.microservices.app.CryptoAPI.v1.dependencies.simply_cuda_aes.AES import CryptoGPU
from Backend.microservices.app.CryptoAPI.v1.config import env

import os


class CryptoManagerGPU:
    __instance = None

    @staticmethod
    def get_instance() -> None:
        if CryptoManagerGPU.__instance is None:

            # Si hay un archivo .env obtiene de ello la variable de entorno
            if env == "dev":
                env_path = find_dotenv()
                load_dotenv(dotenv_path=env_path)
            
            cryptography_key = os.getenv('KEY_CRYPTO_GPU')
            print(cryptography_key)
            
            if not cryptography_key:
                raise ValueError("No se encontró la clave de cifrado en el entorno.")
            
            CryptoManagerGPU.__instance = CryptoGPU(key=cryptography_key)


        # Si hay una replica, evitar volver a obtener las variables o subprocesos!
        return CryptoManagerGPU.__instance

crypto_manager_gpu = CryptoManagerGPU.get_instance()

router = APIRouter()

@router.post('/encrypt', responses=responses_encrypt)
async def Encrypt_GPU(req: Request):

    # Acceder al texto decodificado desde el middleware
    bytes_ = req.state.body

    print(bytes_)

    # Validar que el contenido no esté vacío
    if len(bytes_) == 0 or bytes_.isspace():
        del bytes_
        #print('hubo un error inesperado')
        return Response(content=b'0', media_type='application/octet-stream')

    try:
        # Procesar el texto
        resultado = crypto_manager_gpu.encrypt(bytes_)
        
    except Exception as e:
        #print(f'huno un error: {e}')
        # No se elimina de forma explicita la vairbale resultado, porque si hay un error, no se podra borrar por el error, y generara otro error
        del bytes_
        return Response(content=b'0', media_type='application/octet-stream')

    return Response(content=resultado, media_type='application/octet-stream')


@router.post('/decrypt', responses=responses_decrypt)
async def Decrypt_GPU(req: Request):
    # Acceder al texto decodificado desde el middleware
    bytes_ = req.state.body

    # Validar que el contenido no esté vacío
    if len(bytes_) == 0 or bytes_.isspace():
        del bytes_
        return Response(content=b'0', media_type='application/octet-stream')

    try:
        # Procesar el texto
        #print(bytes_)
        resultado = crypto_manager_gpu.decrypt(bytes_)
        
    except Exception as e:
        # No se elimina de forma explicita la vairbale resultado, porque si hay un error, no se podra borrar por el error, y generara otro error
        del bytes_
        return Response(content=b'0', media_type='application/octet-stream')

    return Response(content=resultado, media_type='application/octet-stream')
