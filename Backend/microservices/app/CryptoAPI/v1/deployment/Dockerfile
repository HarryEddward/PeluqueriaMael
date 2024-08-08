# Usa una imagen base de CUDA
FROM nvidia/cuda:11.4.3-devel-ubuntu20.04

# Establecer variables de entorno para CUDA
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV CUDA_HOME="/usr/local/cuda"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"

# Evita las preguntas interactivas durante la instalación
ARG DEBIAN_FRONTEND=noninteractive

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /peluqueriamael

# Instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip, setuptools, wheel
RUN pip3 install --upgrade pip setuptools wheel

# Verificar que CUDA está configurado correctamente
RUN nvcc --version

# Instalar pycuda por separado
RUN pip3 install numpy==1.24.4
RUN pip3 install pycuda==2024.1

# Instalar paquetes de Python
RUN pip3 install \
    uvicorn \
    gunicorn \
    ujson \
    fastapi \
    redis \
    "fastapi-cache2[redis]" \
    sphinx \
    pyjwt \
    cryptography \
    starlette \
    pytest \
    sphinxawesome-theme \
    httpx \
    termcolor \
    validate-utf8 \
    pyyaml \
    pydantic \
    python-dotenv \
    rethinkdb

# Cambiar al directorio del proyecto de la API de CryptoAPI
WORKDIR /peluqueriamael/Backend/microservices/app/CryptoAPI/v1

# Copiar el script de entrada
COPY ./scripts/entrypoint.sh /peluqueriamael/entrypoint.sh

# Hacer el script de entrada ejecutable
RUN chmod +x /peluqueriamael/entrypoint.sh

# Configurar el script como ENTRYPOINT
#ENTRYPOINT ["/peluqueriamael/entrypoint.sh"]

# Comando por defecto para mantener el contenedor en ejecución
CMD ["tail", "-f", "/dev/null"]