from Backend.microservices.app.conversor.config.config import Config


'''
No se necesita añadir el protocolo, ya que los certificados
ssl determinaran si el protocolo será http o https.

Como gunicorn es para producción 
'''

config = Config()
host = config['host']
port = config['API']['net']['port']

bind = f"{host}:{port}"  # Escucha en todas las interfaces en el puerto 8000
workers = 4  # Número de procesos de trabajadores
worker_class = "uvicorn.workers.UvicornWorker"  # Usar Uvicorn como clase de trabajador
keyfile = "../../../certs/peluqueriamael.com_key.txt"  # Ruta a tu archivo de clave privada
certfile = "../../../certs/peluqueriamael.com_cert/peluqueriamael.com.crt"  # Ruta a tu archivo de certificado