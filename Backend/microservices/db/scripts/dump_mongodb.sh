#!/bin/bash


# Verifica si las variables estan definidas
if [ -z "$USERNAME_MONGODB" ] || [ -z "$PASSWORD_MONGODB" ]; then
    echo "Se necesita definir las 2 variables de entorno."
    exit 1
fi

echo "$USERNAME_MONGODB"
echo "$PASSWORD_MONGODB"

# Contenedor MongoDB
CONATINER_NAME="mongodb_hairdresser"

# Ruta del dump de MongoDB
DUMP_PATH="/home/adrian/Documentos/PeluqueriaMael/Backend/microservices/db/dump"

# Copiar el dump al contenedor de la db
sudo docker cp $DUMP_PATH $CONATINER_NAME:/data/dump

#Ejecutar monogrestore en el contenedor, implmentar las colecciones
sudo docker exec -it $CONATINER_NAME mongorestore --username $USERNAME_MONGODB --password $PASSWORD_MONGODB --authenticationDatabase admin /admin/dump