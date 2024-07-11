#!/bin/bash

# Instalación de paquetes necesarios
sudo apt update
sudo apt install -y python3-pip python3-venv

# Crear y activar el entorno virtual
cd ..
python3 -m venv venv
source venv/bin/activate

# Instalación de paquetes en el entorno virtual
pip install numpy pytest fastapi pydantic uvicorn gunicorn pyjwt pyyaml

# Desactivar el entorno virtual
deactivate
