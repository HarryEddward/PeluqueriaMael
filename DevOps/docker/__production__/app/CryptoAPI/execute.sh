# Directorio root del proyecto a trabajar
cd ../../../../../

sudo docker compose -f ./Backend/microservices/app/CryptoAPI/v1/deployment/docker-compose.yml build

sudo docker compose -f ./Backend/microservices/app/CryptoAPI/v1/deployment/docker-compose.yml up -d