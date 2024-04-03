#!/bin/bash
dc = /docker-compose
ph = ./stacks


docker stack deploy -c $ph$dc.backend.yml nombre_del_stack backend
docker stack deploy -c $ph$dc.database.yml nombre_del_stack database
docker stack deploy -c $ph$dc.frontend.yml nombre_del_stack frontend
