#!/bin/bash
cd ../../../../

FILE=./Backend/microservices/db/deployment/docker-compose.yml
sudo docker compose -f $FILE down
sudo docker compose -f $FILE build
sudo docker compose -f $FILE up -d