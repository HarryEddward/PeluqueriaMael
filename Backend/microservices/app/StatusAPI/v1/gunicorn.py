from Backend.microservices.app.config import net

print('Opened in port:' + net['statusapi']['port'])
bind = f"0.0.0.0:{net['statusapi']['port']}"  # Escucha en todas las interfaces en el puerto 8000
workers = 4  # Número de procesos de trabajadores
worker_class = "uvicorn.workers.UvicornWorker"  # Usar Uvicorn como clase de trabajador
keyfile = "../../../certs/peluqueriamael.com_key.txt"  # Ruta a tu archivo de clave privada
certfile = "../../../certs/peluqueriamael.com_cert/peluqueriamael.com.crt"  # Ruta a tu archivo de certificado