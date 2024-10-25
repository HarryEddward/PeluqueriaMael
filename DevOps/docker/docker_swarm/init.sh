#!/bin/bash

main_path="$(pwd)/../../Backend/microservices"
main_path="$(realpath "$main_path")"
echo "$main_path"
file="docker-compose.yml"

# Función para verificar si Docker Swarm ya está inicializado y si este nodo es un manager
check_swarm_status() {
    if sudo docker info --format '{{.Swarm.LocalNodeState}}' | grep -q "active"; then
        if sudo docker info --format '{{.Swarm.ControlAvailable}}' | grep -q "true"; then
            echo "Este nodo es un manager de Swarm activo."
            return 0
        else
            echo "Swarm está activo, pero este nodo no es un manager."
            return 2
        fi
    else
        echo "Docker Swarm no está activo. Procediendo con la inicialización."
        return 1
    fi
}

# Función para reiniciar Swarm
reset_swarm() {
    echo "Reiniciando Swarm..."
    sudo docker swarm leave --force
    sudo systemctl restart docker
    sleep 5  # Esperar a que Docker se reinicie completamente
    initialize_swarm
}

# Inicializar Swarm
initialize_swarm() {
    echo "Inicializando Swarm..."
    output=$(sudo docker swarm init --advertise-addr $(hostname -I | awk '{print $1}'))
    echo "$output"
    if [ $? -ne 0 ]; then
        echo "Error al inicializar Swarm. Intentando reiniciar Docker..."
        reset_swarm
    fi
}

# Verificar el estado de Swarm
check_swarm_status
status=$?

if [ $status -eq 1 ]; then
    initialize_swarm
elif [ $status -eq 2 ]; then
    echo "Reiniciando Swarm para promover este nodo a manager..."
    reset_swarm
fi

# Verificar nuevamente el estado después de las operaciones
check_swarm_status
status=$?

if [ $status -ne 0 ]; then
    echo "No se pudo establecer este nodo como manager de Swarm. Saliendo."
    exit 1
fi

# Obtener tokens
worker_token=$(sudo docker swarm join-token worker -q)
manager_token=$(sudo docker swarm join-token manager -q)

# Crear el archivo token.txt y escribir los tokens
echo "Worker Token: $worker_token" > token.txt
echo "Manager Token: $manager_token" >> token.txt

# Cambiar los permisos del archivo
sudo chmod 600 token.txt
sudo chown root:root token.txt
sudo mv token.txt /root/

echo "Los tokens han sido guardados en /root/token.txt con acceso restringido."

# Función para desplegar un stack
deploy_stack() {
    local path=$1
    local name=$2
    if [ -f "$path" ]; then
        echo "Desplegando stack $name desde $path"
        sudo docker stack deploy -c "$path" "$name"
    else
        echo "Error: No se encuentra el archivo $path"
    fi
}

# Desplegar stacks
deploy_stack "$main_path/db/deployment/$file" db
deploy_stack "$main_path/proxy/tor/deployment/$file" tor
deploy_stack "$main_path/app/API/v1/deployment/$file" app_API
deploy_stack "$main_path/app/CryptoAPI/v1/deployment/$file" app_CryptoAPI

# Escalar servicios
echo "Escalando servicios..."
sudo docker service scale app_API=2 || echo "Error al escalar app_API"
sudo docker service scale app_APIWS=2 || echo "Error al escalar app_APIWS"

echo "Despliegue completado."