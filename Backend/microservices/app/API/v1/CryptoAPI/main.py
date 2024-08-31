from Backend.microservices.app.API.v1.shared_microservices.cryptoapi.main import encrypt, decrypt

import random
import string
import time



if __name__ == "__main__":

    # Generar la cadena aleatoria
    random_string: str = ''.join(random.choices(string.ascii_letters, k=10))
    
    text: str = random_string
    del random_string

    start_time = time.time()

    encrypted_text: bytes = encrypt(text)
    #print(encrypted_text)

    decrypted_text: str = decrypt(text.encode()).decode()
    #print(decrypted_text)

    end_time = time.time()
    print(f'Execution time: {end_time - start_time}')
