import random
import string

def secrets_generator(length: int = 40):
    """Genera una clave segura para JWT."""
    # Caracteres válidos para la clave segura
    characters = string.ascii_letters + string.digits + '!@#$%^&*()-_=+'
    # Genera la clave segura usando caracteres válidos
    secure_key = ''.join(random.choice(characters) for _ in range(length))
    return secure_key
