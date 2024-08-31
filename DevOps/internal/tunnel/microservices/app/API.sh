#!/bin/bash

# Ruta al archivo de configuración
path_config_yml="./../../../../../Backend/microservices/config.yml"
path_config_log="./../../../../../Backend/microservices/app/API/v1/logs/info.log"
log_level="INFO"
logger_name="tunnel"


# Define la fecha y hora actual
current_datetime=$(date '+%Y-%m-%d %H:%M:%S,%3N')


# Comprobar si yq está instalado
if ! command -v yq &> /dev/null
then
    echo "yq no está instalado. Instálalo para continuar."
    exit 1
fi

# Comprobar si tmole está instalado
if ! command -v tmole &> /dev/null
then
    echo "tmole no está instalado. Instálalo para continuar."
    exit 1
fi

# Extraer el puerto del archivo YAML
query_port=$(yq '.app.API.net.port' "$path_config_yml")

# Verificar si se obtuvo un puerto válido
if [ -z "$query_port" ]
then
    echo "No se pudo obtener el puerto de la configuración. Verifica el archivo YAML."
    exit 1
fi

# Construye el mensaje de log y lo escribe en el archivo
echo "$current_datetime - $logger_name - $log_level - " >> "$path_config_log"

# Ejecutar tmole en segundo plano y redirigir la salida a un archivo
tmole "$query_port" >> "$path_config_log" 2>&1 &

# Obtener el PID del proceso tmole
tmole_pid=$!

# Bucle de espera
while true
do
    # Espera indefinidamente hasta que se reciba una señal de interrupción
    sleep 1
done

kill "$tmole_pid"
