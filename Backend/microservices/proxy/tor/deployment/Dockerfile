# Usa una imagen base de Debian
FROM debian:latest

# Actualiza los paquetes e instala Tor
RUN apt-get update && \
    apt-get install -y tor

# Elimina el archivo o directorio de configuración torrc si existe
RUN rm -rf /etc/tor/torrc

# Copia el archivo de configuración torrc al contenedor en la ruta correcta
COPY torrc /etc/tor

# Establece permisos correctos para el directorio de servicios ocultos
RUN mkdir -p /var/lib/tor/hidden_service && \
    chmod 0700 /var/lib/tor/hidden_service

# Expone el puerto por el que Tor escuchará
EXPOSE 9050

# Inicia el servicio Tor
CMD ["tor"]
