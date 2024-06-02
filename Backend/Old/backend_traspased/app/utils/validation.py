import jwt
import json
from datetime import datetime, UTC, timedelta

SECRET_KEY = '0saud90adapdj2eq08dada0'

def create_token(actualDict: dict):
    # Implementa la lógica para crear el token
    # Aquí deberías usar jwt.encode

    # Verificar si actualDict es un diccionario
    print(actualDict)

    if not isinstance(actualDict, dict):
        raise ValueError("actualDict debe ser un diccionario")

    payload = {
        "exp": datetime.now(UTC) + timedelta(days=30)
    }

    for clave, valor in actualDict.items():
        payload[clave] = valor

    try:
        # Intentar codificar el token
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        print(f'\nToken creado:\n{token}')
        return {
            "info": "Se creo el token",
            "status": "ok",
            "type": "SUCCESS",
            "token": token,
        }
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir al codificar el token
        print(f'Error al codificar el token: {e}')
        return {
            "token": None,
            "status": "no",
            "type": "JWT_CODIFY_ERROR"
        }





def validate_token(token):
    
    try:
        decode_payload = jwt.decode(

            token,
            SECRET_KEY,
            algorithms=['HS256']
        )
        user_ = decode_payload['number_phone']
        psw_ = decode_payload['password']
        expiration = decode_payload['exp']
        expiration_time = datetime.fromtimestamp(expiration)

        time_left = expiration_time - datetime.now()

        print("Token válido")
        print("User:", user_)
        print("Password:", psw_)
        print("Expiración:", expiration)
        print("Expiración:", expiration_time)
        print("Tiempo restante hasta la expiración:", time_left)

        print(f'\n\nToken validado:\n{decode_payload}')
        return {
            "info": "Token valido",
            "status": "ok",
            "type": 'SUCCESS',
            "token": decode_payload,
        }
    
    except jwt.ExpiredSignatureError:
        return {
            "info": "El token expiró!",
            "status": "no",
            "type": 'JWT_EXPIRED_ERROR'
        }

    except jwt.InvalidTokenError:
        return {
            "info": "El token no es el mismo!",
            "status": "no",
            "type": 'JWT_INVALID_TOKEN_ERROR'
        }



def refresh_token(old_token):
    
    global validate_token
    global data

    validate_old_token = validate_token(old_token)
    data = validate_old_token['token']
    print(f'->> {data}')
    data.popitem()
    print(f'->> {data}')

    def refreshIt():

        payload = {
            "user": user,
            "psw": psw,
            "exp": datetime.now(UTC) + timedelta(days=31)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return create_token(data)



    match validate_old_token["status"]:
        case "yes":
            return refreshIt()
        case "no":
            return {
                'info': 'Expiro el token o huvo un problema!',
                'status': "no",
                'type': 'JWT_ERROR'
            }


if __name__ == '__main__':
    print('----------------------------------')
    print('            JWT TOKEN             ')
    print('----------------------------------')

    action = input('\n¿Qué quieres hacer?\n · Crear (c)\n · Renovar (r)\n · Validar (v)\n\n')

    if action == 'c':
        user = input('User:\n')
        psw = input('\nPassword:\n')
        create_token(user, psw)
        
    elif action == 'v':
        token = input('Ingrese el token a validar:\n')
        validate_token(token)

    elif action == 'r':
        token = input('Ingrese el antiguo token:\n')
        refresh_token(token)
