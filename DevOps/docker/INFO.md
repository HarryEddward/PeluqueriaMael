# INFO Docker Containers

To make use correctly running the tests files (sudo ./run.sh), you need
to change the exact Dockerfile of the api, changing the last command (CMD), to: CMD ["tail", "-f", "/dev/null"]

If the conatiner still hard to get up, is that solution if only the case of CryptoAPI. Is the reason for the complex system behind using cuda with python in a non exclusive container dedicated for using python.

Remember if you want change the name of the specific image of the Dockerfile, change in the run.sh the name and also the docker-compose.yml