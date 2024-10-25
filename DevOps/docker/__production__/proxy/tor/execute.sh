# Directorio root del proyecto a trabajar
cd ../../../../../

sudo iptables -A INPUT -p tcp --dport 9050 -j DROP
sleep 3
echo "BUILDING TOR"
sudo docker compose -f ./Backend/microservices/proxy/tor/deployment/docker-compose.yml down
sudo docker compose -f ./Backend/microservices/proxy/tor/deployment/docker-compose.yml build
sudo docker compose -f ./Backend/microservices/proxy/tor/deployment/docker-compose.yml up -d

