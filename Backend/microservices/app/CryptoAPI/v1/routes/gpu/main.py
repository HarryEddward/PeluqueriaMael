from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response

from Backend.microservices.app.CryptoAPI.v1.routes.gpu.responses import (
    responses_encrypt,
    responses_decrypt
)

router = APIRouter()


@router.get('/encrypt', responses=responses_encrypt)
async def Encrypt_GPU(req: Request):
    pass

@router.get('/decrypt', responses=responses_decrypt)
async def Decrypt_GPU(req: Request):
    pass
