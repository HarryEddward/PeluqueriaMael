FROM python:latest  

# Instala las dependencias
RUN pip install pymongo \
    "fastapi-cache2[redis]" \
    pyjwt \
    fastapi \
    gunicorn \
    uvicorn \
    numba \
    pydantic_extra_types \
    phonenumbers \
    sphinx \
    ujson \
    pyyaml \
    pydantic \
    pydantic[email] \
    python-dotenv \
    rethinkdb

WORKDIR /peluqueriamael/Backend/microservices/app/API/v1


#CMD ["tail", "-f", "/dev/null"]
#CMD ["./execute.sh"]