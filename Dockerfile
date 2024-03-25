FROM python:3.9

#RUN apt-get update && apt-get install -y \
#    python3 \
#    python3-pip

COPY /API /app
COPY /API/requirements.txt /tmp/

ENV JWT_SECRET=kjsahdksahdsa89dyhsahdsahdysa98dysadhisad89sa9dhsadh9say
ENV version=1.12

RUN pip install --no-cache-dir -r /tmp/requirements.txt
#ARG TEXT_EDITOR=nano

WORKDIR /app

CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "server:app", "--bind", "0.0.0.0:8000" ]

#ENTRYPOINT ./DevOps/scripts/docker/ENTRYPOINT.sh