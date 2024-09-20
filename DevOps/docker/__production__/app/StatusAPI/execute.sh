#!/bin/bash
# Directorio root del proyecto a trabajar
cd ../../../../../

sudo docker compose -f ./Backend/microservices/app/StatusAPI/v1/deployment/docker-compose.yml down
sudo docker compose -f ./Backend/microservices/app/StatusAPI/v1/deployment/docker-compose.yml build
sudo docker compose -f ./Backend/microservices/app/StatusAPI/v1/deployment/docker-compose.yml up -d