#!/bin/bash
# Directorio root del proyecto a trabajar
cd ../../../../../

echo "BUILDING CryptoAPI/v1"
sudo docker compose -f ./Backend/microservices/app/CryptoAPI/v1/deployment/docker-compose.yml down
sudo docker compose -f ./Backend/microservices/app/CryptoAPI/v1/deployment/docker-compose.yml build
sudo docker compose -f ./Backend/microservices/app/CryptoAPI/v1/deployment/docker-compose.yml up -d