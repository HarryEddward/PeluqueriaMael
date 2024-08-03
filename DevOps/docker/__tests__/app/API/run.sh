#!/bin/bash

# Directorio root del proyecto a trabajar
cd ../../../../../

# Nombre de la imagen
IMAGE_NAME="peluqueriamael_app_api"

# Nombre del contenedor (debe ser igual al nombre del servicio en docker-compose.yml)
CONTAINER_NAME="deployment_peluqueriamael_app_api"

# Verificar si se ha proporcionado un archivo docker-compose.yml personalizado
if [ $# -eq 1 ]; then
    COMPOSE_FILE=$1
else
    COMPOSE_FILE="/home/adrian/Documentos/PeluqueriaMael/Backend/microservices/app/API/v1/deployment/docker-compose.yml"
fi

# Mensaje de inicio
echo "Iniciando el proceso de despliegue usando el archivo ${COMPOSE_FILE}..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker no está instalado. Por favor, instala Docker y vuelve a intentarlo."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker compose &> /dev/null; then
    echo "Docker Compose no está instalado. Por favor, instala Docker Compose y vuelve a intentarlo."
    exit 1
fi

# Buscar y detener el contenedor en ejecución si existe
RUNNING_CONTAINER=$(docker ps -q -f name=$CONTAINER_NAME)
if [ ! -z "$RUNNING_CONTAINER" ]; then
    echo "Deteniendo y eliminando el contenedor en ejecución con el nombre $CONTAINER_NAME..."
    docker compose -f $COMPOSE_FILE down
    # Alternativamente, podrías usar:
    # docker stop $RUNNING_CONTAINER && docker rm $RUNNING_CONTAINER
fi

# Buscar imagen existente y eliminarla si existe
EXISTING_IMAGE=$(docker images -q $IMAGE_NAME)
if [ ! -z "$EXISTING_IMAGE" ]; then
    echo "La imagen $IMAGE_NAME ya existe. Eliminándola..."
    docker rmi -f $EXISTING_IMAGE
    sleep 5
fi

# Construir la imagen
echo "Construyendo la imagen de Docker..."
docker compose -f $COMPOSE_FILE build

# Verificar si la construcción fue exitosa
if [ $? -ne 0 ]; then
    echo "La construcción de la imagen falló. Por favor, revisa los errores anteriores."
    exit 1
fi

# Levantar el contenedor
echo "Levantando el contenedor..."
docker compose -f $COMPOSE_FILE up -d

# Verificar si el contenedor se levantó correctamente
if [ $? -ne 0 ]; then
    echo "Fallo al levantar el contenedor. Por favor, revisa los errores anteriores."
    exit 1
fi

# Mensaje de éxito
echo "El contenedor se ha levantado correctamente y está ejecutándose en segundo plano."

# Esperar a que el contenedor esté en ejecución antes de intentar acceder a la terminal
sleep 5

# Acceder a la terminal del contenedor
CONTAINER_ID=$(docker compose -f $COMPOSE_FILE ps -q)
if [ ! -z "$CONTAINER_ID" ]; then
    echo "Accediendo a la terminal del contenedor con ID $CONTAINER_ID..."

    # Se implementa las variables de entorno directamente por bash por problemas internos de docker al intentar implementar variables de entorno en el contenedor
    sudo docker exec -it $CONTAINER_ID bash
else
    echo "El contenedor no está en ejecución. No se puede acceder a la terminal."
fi

# Fin del script
echo "Proceso de despliegue completado."
