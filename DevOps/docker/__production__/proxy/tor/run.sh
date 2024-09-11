#!/bin/bash

# Directorio root del proyecto a trabajar
cd ../../../../../

# Nombre de la imagen
IMAGE_NAME="tor_proxy"

# Nombre del contenedor (debe ser igual al nombre del servicio en docker-compose.yml)
CONTAINER_NAME="deployment_tor_proxy"

# Verificar si se ha proporcionado un archivo docker-compose.yml personalizado
if [ $# -eq 1 ]; then
    COMPOSE_FILE=$1
else
    echo "--------------> $pwd"
    COMPOSE_FILE="./Backend/microservices/proxy/tor/deployment/docker-compose.yml"
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
RUNNING_CONTAINER=$(docker ps -q -f name="$IMAGE_NAME")
echo "$RUNNING_CONTAINER <------------"
if [ ! -z "$RUNNING_CONTAINER" ]; then
    echo "Deteniendo y eliminando el contenedor en ejecución con el nombre $CONTAINER_NAME..."
    #docker stop $COMPOSE_FILE
    #docker rm $COMPOSE_FILE
    #sleep 10
    #echo "docker compose -f $COMPOSE_FILE down <---------------------"
    docker compose -f $COMPOSE_FILE down --remove-orphans
    sleep 5
    # Alternativamente, podrías usar:
    # docker stop $RUNNING_CONTAINER && docker rm $RUNNING_CONTAINER
fi

# Buscar imagen existente y eliminarla si existe
EXISTING_IMAGE=$(docker images -q $IMAGE_NAME)
if [ ! -z "$EXISTING_IMAGE" ]; then
    echo "La imagen $IMAGE_NAME ya existe. Eliminándola..."
    docker rmi -f $EXISTING_IMAGE
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

CONTAINER_ID=$(docker compose -f $COMPOSE_FILE ps -q)
if [ ! -z "$CONTAINER_ID" ]; then
    sudo docker ps
else
    echo "El contenedor no está en ejecución. No se puede acceder a la terminal."
fi

# Mensaje de éxito
echo "El contenedor se ha levantado correctamente y está ejecutándose en segundo plano."

# Fin del script
echo "Proceso de despliegue completado."
