import jwt
import datetime
import os
import time



'''
Cuando vaya a produccion los microservicios pensar sobre el secretos del jwt,
añadirlo en el dockerfile, para subirlo al swarm de forma adecuada
'''
#os.getenv("JWT_SECRET")
#print(SECRET_KEY)



class JWToken:
    
    SECRET_KEY = "#@9d0wjd0jih2qhd09h09hdwaodopah099da%"


    @classmethod
    def create(cls, payload: dict, secret: str = None):
        
        try:
            if secret is None:
                secret = cls.SECRET_KEY

            exp_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=30)
            token = jwt.encode(
                payload={
                    "info": payload,
                    "exp": exp_time
                },
                key=secret,
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
    def check(cls, token, secret: str = None):
        try:
            if secret is None:
                secret = cls.SECRET_KEY

            decoded_payload = jwt.decode(token, secret, algorithms=['HS256'])
            return {
                "info": "Creado con éxito el token",
                "status": "ok",
                "type": "SUCCESS",
                "data": decoded_payload
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
