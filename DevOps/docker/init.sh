
main_path=../../Backend/microservices
file=docker-compose.yml

sudo docker stack deploy -c $main_path/db/$file db
sudo docker stack deploy -c $main_path/app/$file app
sudo docker stack deploy -c $main_path/web/$file web

sudo docker service scale app_API=2
sudo docker service scale app_APIWS=2
sudo docker service scale app_CryptoAPI=2
sudo docker service scale app_StatusAPI=2