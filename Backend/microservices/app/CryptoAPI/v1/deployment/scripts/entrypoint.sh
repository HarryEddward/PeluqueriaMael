#!/bin/bash
# Establecer el PATH para CUDA
export PATH=/usr/local/cuda/bin:$PATH
# Ejecutar el comando proporcionado al contenedor
exec "$@"
