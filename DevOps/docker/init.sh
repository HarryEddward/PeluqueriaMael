
main_path=../../Backend/microservices

sudo docker stack deploy -c $main_path/db/docker-compose.yml db
sudo docker stack deploy -c $main_path/app/docker-compose.yml app
sudo docker stack deploy -c $main_path/web/docker-compose.yml web

sudo docker service scale app_API=2
sudo docker service scale app_APIWS=2
sudo docker service scale app_CryptoAPI=2
sudo docker service scale app_StatusAPI=2