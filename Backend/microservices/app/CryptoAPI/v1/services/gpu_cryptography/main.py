from Backend.microservices.app.CryptoAPI.v1.dependencies.simply_cuda_aes.AES import AES, CryptoGPU
from dotenv import load_dotenv, find_dotenv
import numpy as np

load_dotenv()



gpu = CryptoGPU()

encrypted = gpu.encrypt('Hola')
decrypted = gpu.decrypt(encrypted)

import time

start_time = time.time()

for i in range(1000):
    encrypted = gpu.encrypt('Hola')
    decrypted = gpu.decrypt(encrypted)

end_time = time.time()

print(f'Time: {end_time-start_time}')