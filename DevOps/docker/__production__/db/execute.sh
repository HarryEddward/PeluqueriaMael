#!/bin/bash
cd ../../../../

FILE=./Backend/microservices/db/deployment/docker-compose.yml
echo "BUILDING DB"
sudo docker compose -f $FILE down
sudo docker compose -f $FILE build
sudo docker compose -f $FILE up -d