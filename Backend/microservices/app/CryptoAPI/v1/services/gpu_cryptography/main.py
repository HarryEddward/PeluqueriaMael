from Backend.microservices.app.CryptoAPI.v1.dependencies.CUDA_AES_main.AES import AES
from dotenv import load_dotenv, find_dotenv


find_dotenv()


def encrypt(text: str) -> str:

    text = text.encode('utf-8')
    compute = AES()
    AES.encrypt_gpu()