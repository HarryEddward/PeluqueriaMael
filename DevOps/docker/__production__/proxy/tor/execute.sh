# Directorio root del proyecto a trabajar
cd ../../../../../

sudo docker compose -f ./Backend/microservices/proxy/tor/deployment/docker-compose.yml build

sudo docker compose -f ./Backend/microservices/proxy/tor/deployment/docker-compose.yml up -d
