import jwt
import datetime
import os
import time

#SECRET_KEY = os.environ["JWT_SECRET"]
#print(SECRET_KEY)

class JWToken:
    
    @classmethod
    def create(cls, payload):
        try:
            exp_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=5)
            token = jwt.encode(
                payload={
                    "info": payload,
                    "exp": exp_time
                },
                key=SECRET_KEY,
                algorithm='HS256'
            )
            return {
                "info": "Token generado exitosamente",
                "status": "ok",
                "type": "SUCCESS",
                "token": token
            }
        except Exception as e:
            return {
                "info": str(e),
                "status": "no",
                "type": "JWT_CODIFY_ERROR"
            }

    
    @classmethod
    def check(cls, token):
        try:
            decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded_payload
        except jwt.ExpiredSignatureError:
            return {
                "info": "Token JWT expirado. Por favor, genere uno nuevo.",
                "status": "no",
                "type": "JWT_EXPIRED_ERROR"
            }
        except jwt.InvalidTokenError:
            return {
                "info": "Token JWT inválido. No se pudo decodificar.",
                "status": "no",
                "type": "JWT_CODIFY_ERROR"
            }

    @classmethod
    def renew_date(cls, old_token):
        try:
            payload = cls.check(old_token)
            if payload.get("info"):
                new_token = cls.create(payload["info"])
                return new_token
            else:
                return {
                    'info': 'El token ha expirado o hubo un problema!',
                    'status': "no",
                    'type': 'JWT_ERROR'
                }
        except jwt.ExpiredSignatureError:
            return {
                "info": "Token JWT expirado. Por favor, genere uno nuevo.",
                "status": "no",
                "type": "JWT_EXPIRED_ERROR"
            }
        except jwt.InvalidTokenError:
            return {
                "info": "Token JWT inválido. No se pudo decodificar.",
                "status": "no",
                "type": "JWT_CODIFY_ERROR"
            }



if __name__ == "__main__":
    payload_data = {
        "user_id": 123,
        "role": "admin"
    }

    # Crea un token
    token = JWToken.create(payload_data)
    print("Token generado:", token, '\n')

    # Decodifica el token
    decoded_token = JWToken.check(token["token"])
    print("Token decodificado:", decoded_token, '\n')
    time.sleep(1)

    # Refresca el token (opcional)
    refreshed_token = JWToken.renew_date(token["token"])
    print("Token refrescado:", refreshed_token, '\n')

    # Decodifica el token refrescado
    decoded_refreshed_token = JWToken.check(refreshed_token["token"])
    print("Token refrescado decodificado:", decoded_refreshed_token, '\n')

    time.sleep(6)

    # Verifica el token refrescado nuevamente
    decoded_token_after_expiry = JWToken.check(refreshed_token["token"])
    print("Token refrescado decodificado después de la expiración:", decoded_token_after_expiry, '\n')
