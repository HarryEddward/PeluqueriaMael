from Backend.microservices.conversor.config.config import Config


'''
No se necesita añadir el protocolo, ya que los certificados
ssl determinaran si el protocolo será http o https.

Como gunicorn es para producción 
'''

configFile = Config()
host = configFile['host']
port = configFile['app']['CryptoAPI']['net']['port']
#ssl = configFile['ssl']
#ssl_cert = ssl['cert']
#ssl_key = ssl['key']

bind = f"{host}:{port}"  # Escucha en todas las interfaces en el puerto 8000
print('--->', bind)
workers = 4  # Número de procesos de trabajadores
worker_class = "uvicorn.workers.UvicornWorker"  # Usar Uvicorn como clase de trabajador
#keyfile = ssl_key  # Ruta a tu archivo de clave privada
#certfile = ssl_cert  # Ruta a tu archivo de certificado