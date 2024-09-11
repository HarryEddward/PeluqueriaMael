# Usa una imagen base de Debian o Ubuntu
FROM debian:latest

# Actualiza los paquetes e instala Tor
RUN apt-get update && \
    apt-get install -y tor

# Expone el puerto por el que Tor escuchará
EXPOSE 9050

# Inicia el servicio Tor
CMD ["tor"]
