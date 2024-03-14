#!/bin/bash

# Obtener la ruta del directorio del script actual
DIR_ACTUAL="$(dirname "$0")"

# Navegar al directorio anterior
cd "$DIR_ACTUAL/.."

# Exportar PYTHONPATH
export PYTHONPATH="/Users/yeray/Downloads/Backend_Peluqueria_EGO/"

# Ruta al script de Python en el directorio anterior
SCRIPT_PYTHON="./re_schulde.py"

# Ejecutar el script de Python y redirigir la salida estándar y de error a un archivo
python3 "$SCRIPT_PYTHON"

# Aquí puedes continuar con el resto de tu script shell...
