#!/bin/bash

kubectl apply -f pods/backend/deployment-fastapi.yaml
kubectl apply -f pods/backend/service-fastapi.yaml