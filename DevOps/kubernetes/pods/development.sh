#!/bin/bash


DEPLOY = "/deployment/sh/deploy.sh"
DISCONNECT = "/deployment/sh/disconnect.sh"


# Obtener el comando pasado como argumento al script
comando="$1"

# Verificar si el comando contiene la palabra "create"
if echo "$comando" | grep -q "create"; then
    # Ejecutar los 3 comandos de arriba
    sh ./backend/$DEPLOY
    sh ./database/$DEPLOY
    sh ./frontend/$DEPLOY
    kubectl apply -f namespace.yaml

elif echo "$comando" | grep -q "destroy"; then
    # Ejecutar los 3 comandos de abajo
    sh ./backend/$DISCONNECT
    sh ./database/$DISCONNECT
    sh ./frontend/$DISCONNECT
else
    echo "-- Comando inválido: Solo se admite 'create' o 'destroy' --"
    exit 1
fi
