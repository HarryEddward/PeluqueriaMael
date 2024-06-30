FROM python:latest

# Establecer el directorio de trabajo dentro del contenedor
COPY /../../../../../Backend /peluqueriamael
COPY /../../../../../__init__.py /peluqueriamael
COPY /../../../../../LICENSE /peluqueriamael
COPY /../../../../../README.md /peluqueriamael

WORKDIR /Backend/microservices/app/API/v1

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["./init.sh"]