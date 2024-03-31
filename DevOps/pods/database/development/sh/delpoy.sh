#!/bin/bash

kubectl apply -f pods/backend/deployment-mongo.yaml
kubectl apply -f pods/backend/service-mongo.yaml