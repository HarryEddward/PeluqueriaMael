#!/bin/bash

# Copiar el archivo startup.service a la ruta de systemd
cp ./files/startup.service /etc/systemd/system/

# Verificar si la copia fue exitosa
if [ $? -eq 0 ]; then
    echo "OK"
    sudo systemctl daemon-reload
    sudo systemctl enable startup.service
    sudo systemctl start startup.service

else
    echo "ERROR: La copia del archivo startup.service ha fallado"
fi
